#!/usr/bin/env python3
"""
adv-validate.py — Validator for the ADV Data Model v2.0

Validates:
  1) DCAT wrapper (dataset self-description) against model/dsp-wrapper-shapes.ttl
  2) Domain content against the appropriate profile SHACL (e.g., profiles/observation/shape.ttl)
  3) Cross-check wrapper <-> content: adv:profileId vs. content @type (upstream class)

Usage examples:
  # Validate wrapper + content with automatic profile detection from the wrapper:
  python validate/adv-validate.py \
    --wrapper offers/offer.sample.jsonld \
    --content profiles/observation/content.sample.jsonld

  # (Optional) Override default shapes:
  python validate/adv-validate.py \
    --wrapper offers/offer.sample.jsonld \
    --content profiles/observation/content.sample.jsonld \
    --wrapper-shapes model/dsp-wrapper-shapes.ttl \
    --profile-shapes profiles/observation/shape.ttl

Exit codes:
  0 = All validations passed
  1 = Wrapper failed
  2 = Content failed
  3 = Both failed
  4 = Usage / file / runtime error

Requirements:
  pip install rdflib pyshacl

This script assumes the standard repo layout:
  model/dsp-wrapper-shapes.ttl
  profiles/<profile_name>/shape.ttl
Profile name is inferred from the wrapper's `adv:profileId` literal
(e.g., "adv.observation" -> "observation").
"""

import argparse
import os
import sys
from pathlib import Path

from rdflib import Graph, Namespace, Literal, URIRef
from rdflib.namespace import RDF

try:
    from pyshacl import validate as shacl_validate
except Exception as e:
    sys.stderr.write(f"[ERROR] pyshACL is required. Install with: pip install pyshacl\nDetails: {e}\n")
    sys.exit(4)

ADV = Namespace("https://w3id.org/adv/core#")

# Upstream class URIs used by each ADV profile.
# Updated in v2.0 to reference actual SOSA/SAREF4AGRI/FOODIE classes.
SOSA = Namespace("http://www.w3.org/ns/sosa/")
SAREF4AGRI = Namespace("https://saref.etsi.org/saref4agri/")
FOODIE = Namespace("http://foodie-cloud.com/model/foodie#")

PROFILE_TO_CLASS = {
    "adv.observation":  str(SOSA.Observation),
    "adv.parcel-crop":  str(SAREF4AGRI.Parcel),
    "adv.intervention": str(FOODIE.Intervention),
    "adv.animal":       str(SAREF4AGRI.Animal),
    "adv.alert":        str(FOODIE.Alert),
}

# -------------------------
# Helpers
# -------------------------

def infer_format(path: str):
    ext = path.lower().split(".")[-1]
    if ext in ("jsonld", "json"):
        return "json-ld"
    if ext in ("ttl", "turtle"):
        return "turtle"
    if ext in ("nt", "ntriples"):
        return "nt"
    if ext in ("nq", "nquads"):
        return "nquads"
    if ext in ("trig",):
        return "trig"
    if ext in ("rdf", "xml"):
        return "xml"
    return None


def load_graph(path: str) -> Graph:
    g = Graph()
    fmt = infer_format(path)
    try:
        g.parse(path, format=fmt)
    except Exception as e:
        raise RuntimeError(f"Failed to parse RDF file: {path}\n{e}")
    return g


def run_shacl(data_graph: Graph, shapes_graph: Graph, name: str) -> tuple[bool, str]:
    conforms, results_graph, results_text = shacl_validate(
        data_graph=data_graph,
        shacl_graph=shapes_graph,
        inference="rdfs",
        allow_infos=True,
        allow_warnings=True,
        js=False,
        meta_shacl=False,
        advanced=True,
        debug=False,
    )
    header = f"=== Validation Report: {name} ==="
    report = f"{header}\n{results_text.strip()}\n"
    return bool(conforms), report


def get_profile_id(wrapper_graph: Graph) -> str | None:
    for s, p, o in wrapper_graph.triples((None, ADV.profileId, None)):
        if isinstance(o, Literal):
            return str(o)
        return str(o)
    return None


def profile_to_folder(profile_id: str) -> str | None:
    """
    Convert "adv.observation" -> "observation"
            "adv.parcel-crop" -> "parcel-crop"
    """
    if not profile_id:
        return None
    if profile_id.startswith("adv."):
        return profile_id.split("adv.", 1)[1]
    return profile_id


def safe_path(*parts) -> str:
    return str(Path(*parts).as_posix())


def get_types(content_graph: Graph) -> set[str]:
    """Collects all RDF types present in the content graph (as strings)."""
    return {str(o) for _, _, o in content_graph.triples((None, RDF.type, None))}


# -------------------------
# CLI
# -------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Validate DCAT wrapper and domain content against ADV SHACL shapes."
    )
    parser.add_argument("--wrapper", required=True, help="Path to DCAT wrapper JSON-LD (dcat:Dataset).")
    parser.add_argument("--content", required=True, help="Path to domain content JSON-LD.")
    parser.add_argument("--wrapper-shapes", default="model/dsp-wrapper-shapes.ttl",
                        help="Path to DCAT wrapper SHACL shapes TTL.")
    # Keep legacy flag for backward compat
    parser.add_argument("--ids-shapes", default=None,
                        help="(Deprecated) Alias for --wrapper-shapes. Use --wrapper-shapes instead.")
    parser.add_argument("--profile-shapes", default=None,
                        help="Path to profile SHACL shapes TTL. If omitted, inferred from wrapper's adv:profileId.")
    args = parser.parse_args()

    # Resolve wrapper shapes path (prefer new flag, fallback to legacy)
    wrapper_shapes_path = args.wrapper_shapes
    if args.ids_shapes:
        sys.stderr.write("[WARN] --ids-shapes is deprecated. Use --wrapper-shapes instead.\n")
        wrapper_shapes_path = args.ids_shapes

    # Basic file checks
    for p in [args.wrapper, args.content, wrapper_shapes_path]:
        if not os.path.exists(p):
            sys.stderr.write(f"[ERROR] File not found: {p}\n")
            sys.exit(4)

    # Load wrapper and run DCAT wrapper SHACL
    try:
        wrapper_graph = load_graph(args.wrapper)
        wrapper_shapes_graph = load_graph(wrapper_shapes_path)
    except Exception as e:
        sys.stderr.write(f"[ERROR] {e}\n")
        sys.exit(4)

    wrapper_ok, wrapper_report = run_shacl(wrapper_graph, wrapper_shapes_graph, "DCAT Wrapper")
    print(wrapper_report)

    # Determine profile shapes path if not provided
    profile_shapes_path = args.profile_shapes
    if not profile_shapes_path:
        profile_id = get_profile_id(wrapper_graph)
        if not profile_id:
            sys.stderr.write("[ERROR] Could not find adv:profileId in wrapper. Provide --profile-shapes explicitly.\n")
            sys.exit(4)
        folder = profile_to_folder(profile_id)
        profile_shapes_path = safe_path("profiles", folder, "shape.ttl")
        if not os.path.exists(profile_shapes_path):
            sys.stderr.write(f"[ERROR] Inferred profile SHACL not found: {profile_shapes_path}\n"
                             f"       (Inferred from adv:profileId='{profile_id}')\n"
                             f"       Provide --profile-shapes explicitly.\n")
            sys.exit(4)

    # Load content and run Profile SHACL
    try:
        content_graph = load_graph(args.content)
        profile_shapes_graph = load_graph(profile_shapes_path)
    except Exception as e:
        sys.stderr.write(f"[ERROR] {e}\n")
        sys.exit(4)

    content_ok, content_report = run_shacl(content_graph, profile_shapes_graph, "Domain Content")
    print(content_report)

    # -------- Wrapper <-> Content Cross-check --------
    try:
        profile_id = get_profile_id(wrapper_graph)
        expected_class = PROFILE_TO_CLASS.get(profile_id)
        if expected_class:
            content_types = get_types(content_graph)
            if expected_class not in content_types:
                sys.stderr.write(
                    "[ERROR] Wrapper/content mismatch:\n"
                    f"        adv:profileId = '{profile_id}' expects content @type '{expected_class}'.\n"
                    f"        Found @type values: {sorted(content_types)}\n"
                )
                content_ok = False
    except Exception as e:
        sys.stderr.write(f"[WARN] Cross-check skipped due to unexpected error: {e}\n")
    # ---------------------------------------------------

    # Exit codes
    if wrapper_ok and content_ok:
        print("All checks passed.")
        sys.exit(0)
    if not wrapper_ok and content_ok:
        print("Wrapper failed. Content passed.")
        sys.exit(1)
    if wrapper_ok and not content_ok:
        print("Content failed. Wrapper passed.")
        sys.exit(2)
    print("Both wrapper and content failed.")
    sys.exit(3)


if __name__ == "__main__":
    main()
