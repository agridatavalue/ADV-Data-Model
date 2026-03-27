#!/usr/bin/env python3
"""
adv-validate.py — Simple validator for the ADV Data Model

Validates:
  1) IDS wrapper (offer) against model/ids/ids-wrapper-shapes.ttl
  2) AIM content against the appropriate profile SHACL (e.g., profiles/observation/shape.ttl)
  3) (New in v1.1) Cross-check wrapper ↔ content: adv:profileId vs. content @type (AIM class)

Usage examples:
  # Validate wrapper + content with automatic profile detection from the wrapper:
  python validate/adv-validate.py \
    --wrapper offers/offer.sample.jsonld \
    --content profiles/observation/content.sample.jsonld

  # (Optional) Override default shapes:
  python validate/adv-validate.py \
    --wrapper offers/offer.sample.jsonld \
    --content profiles/observation/content.sample.jsonld \
    --ids-shapes model/ids/ids-wrapper-shapes.ttl \
    --profile-shapes profiles/observation/shape.ttl

Exit codes:
  0 = All validations passed
  1 = IDS wrapper failed
  2 = Content failed
  3 = Both failed
  4 = Usage / file / runtime error

Requirements:
  pip install rdflib pyshacl

This script assumes the standard repo layout:
  model/ids/ids-wrapper-shapes.ttl
  profiles/<profile_name>/shape.ttl
Profile name is inferred from the wrapper's `adv:profileId` literal (e.g., "adv.observation" → "observation").
"""

import argparse
import os
import sys
from pathlib import Path

from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF

try:
    from pyshacl import validate as shacl_validate
except Exception as e:
    sys.stderr.write(f"[ERROR] pyshACL is required. Install with: pip install pyshacl\nDetails: {e}\n")
    sys.exit(4)

ADV = Namespace("https://w3id.org/adv/core#")
AIM = Namespace("https://w3id.org/aim#")  # (New) Needed for cross-checks

# (New) Map ADV profile IDs to expected AIM classes for a lightweight cross-check.
PROFILE_TO_AIM = {
    "adv.observation": str(AIM.Observation),
    "adv.parcel-crop": str(AIM.FeatureOfInterest),
    "adv.intervention": str(AIM.Activity),
    "adv.animal":      str(AIM.Animal),
    "adv.alert":       str(AIM.Alert),
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
    # Fallback: rdflib can sometimes guess
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
    # Return the literal string value of adv:profileId if present
    for s, p, o in wrapper_graph.triples((None, ADV.profileId, None)):
        if isinstance(o, Literal):
            return str(o)
        # If someone provided it as IRI (not recommended), still try to read
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
    return profile_id  # fallback


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
        description="Validate IDS wrapper and AIM content against ADV SHACL shapes."
    )
    parser.add_argument("--wrapper", required=True, help="Path to IDS wrapper JSON-LD (ids:Resource).")
    parser.add_argument("--content", required=True, help="Path to AIM content JSON-LD.")
    parser.add_argument("--ids-shapes", default="model/ids/ids-wrapper-shapes.ttl",
                        help="Path to IDS wrapper SHACL shapes TTL.")
    parser.add_argument("--profile-shapes", default=None,
                        help="Path to profile SHACL shapes TTL. If omitted, inferred from wrapper's adv:profileId.")
    args = parser.parse_args()

    # Basic file checks
    for p in [args.wrapper, args.content, args.ids_shapes]:
        if not os.path.exists(p):
            sys.stderr.write(f"[ERROR] File not found: {p}\n")
            sys.exit(4)

    # Load wrapper and run IDS SHACL
    try:
        wrapper_graph = load_graph(args.wrapper)
        ids_shapes_graph = load_graph(args.ids_shapes)
    except Exception as e:
        sys.stderr.write(f"[ERROR] {e}\n")
        sys.exit(4)

    wrapper_ok, wrapper_report = run_shacl(wrapper_graph, ids_shapes_graph, "IDS Wrapper")
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

    content_ok, content_report = run_shacl(content_graph, profile_shapes_graph, "AIM Content")
    print(content_report)

    # -------- New in v1.1: Wrapper ↔ Content Cross-check --------
    # If we can resolve the profile → expected AIM class, verify that the content
    # contains at least one instance of that class. This is a pragmatic sanity check;
    # SHACL still does the heavy lifting for constraints.
    try:
        profile_id = get_profile_id(wrapper_graph)
        expected_aim_class = PROFILE_TO_AIM.get(profile_id)
        if expected_aim_class:
            content_types = get_types(content_graph)
            if expected_aim_class not in content_types:
                sys.stderr.write(
                    "[ERROR] Wrapper/content mismatch:\n"
                    f"        adv:profileId = '{profile_id}' expects content @type '{expected_aim_class}'.\n"
                    f"        Found @type values: {sorted(content_types)}\n"
                )
                content_ok = False
    except Exception as e:
        # Don't crash the run; report and let SHACL results decide.
        sys.stderr.write(f"[WARN] Cross-check skipped due to unexpected error: {e}\n")
    # -------------------------------------------------------------

    # Exit codes
    if wrapper_ok and content_ok:
        print("✅ All checks passed.")
        sys.exit(0)
    if not wrapper_ok and content_ok:
        print("❌ Wrapper failed. Content passed.")
        sys.exit(1)
    if wrapper_ok and not content_ok:
        print("❌ Content failed. Wrapper passed.")
        sys.exit(2)
    print("❌ Both wrapper and content failed.")
    sys.exit(3)


if __name__ == "__main__":
    main()
