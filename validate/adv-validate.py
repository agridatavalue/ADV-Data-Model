#!/usr/bin/env python3
"""
adv-validate.py — Validator for the ADV Data Model v2.0

Validates ADV data packages in three modes:

  Full mode (wrapper + content):
    Validates the DCAT wrapper, the domain content, and cross-checks them.

  Content-only mode (--content-only):
    Validates domain content against a profile SHACL shape without a wrapper.
    Useful during development when you haven't created the offer yet.

Usage examples:
  # Full validation (wrapper + content):
  python validate/adv-validate.py \\
    --wrapper offers/offer.sample.jsonld \\
    --content profiles/observation/content.sample.jsonld

  # Content-only validation (no wrapper needed):
  python validate/adv-validate.py \\
    --content profiles/observation/content.sample.jsonld \\
    --content-only --profile observation

  # Override default shapes:
  python validate/adv-validate.py \\
    --wrapper offers/offer.sample.jsonld \\
    --content profiles/observation/content.sample.jsonld \\
    --wrapper-shapes model/dsp-wrapper-shapes.ttl \\
    --profile-shapes profiles/observation/shape.ttl

Exit codes:
  0 = All validations passed
  1 = Wrapper failed (full mode only)
  2 = Content failed
  3 = Both failed (full mode only)
  4 = Usage / file / runtime error

Requirements:
  pip install -r validate/requirements.txt
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

# Short profile names for --content-only mode
PROFILE_SHORT_NAMES = {
    "observation":  "adv.observation",
    "parcel-crop":  "adv.parcel-crop",
    "intervention": "adv.intervention",
    "animal":       "adv.animal",
    "alert":        "adv.alert",
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
    if not profile_id:
        return None
    if profile_id.startswith("adv."):
        return profile_id.split("adv.", 1)[1]
    return profile_id


def safe_path(*parts) -> str:
    return str(Path(*parts).as_posix())


def get_types(content_graph: Graph) -> set[str]:
    return {str(o) for _, _, o in content_graph.triples((None, RDF.type, None))}


# -------------------------
# CLI
# -------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Validate DCAT wrapper and domain content against ADV SHACL shapes."
    )
    parser.add_argument("--wrapper", default=None,
                        help="Path to DCAT wrapper JSON-LD (dcat:Dataset). Required unless --content-only.")
    parser.add_argument("--content", required=True,
                        help="Path to domain content JSON-LD.")
    parser.add_argument("--content-only", action="store_true",
                        help="Validate content only (no wrapper). Requires --profile or --profile-shapes.")
    parser.add_argument("--profile", default=None,
                        choices=list(PROFILE_SHORT_NAMES.keys()),
                        help="Profile name for --content-only mode (e.g., observation, animal).")
    parser.add_argument("--wrapper-shapes", default="model/dsp-wrapper-shapes.ttl",
                        help="Path to DCAT wrapper SHACL shapes TTL.")
    parser.add_argument("--ids-shapes", default=None,
                        help="(Deprecated) Alias for --wrapper-shapes.")
    parser.add_argument("--profile-shapes", default=None,
                        help="Path to profile SHACL shapes TTL. If omitted, inferred from wrapper or --profile.")
    args = parser.parse_args()

    # ---- Content-only mode ----
    if args.content_only:
        return run_content_only(args)

    # ---- Full mode: require wrapper ----
    if not args.wrapper:
        sys.stderr.write("[ERROR] --wrapper is required unless using --content-only mode.\n")
        sys.exit(4)

    return run_full(args)


def run_content_only(args):
    """Validate content against profile SHACL only. No wrapper needed."""
    # Determine profile shapes
    profile_shapes_path = args.profile_shapes
    if not profile_shapes_path:
        if not args.profile:
            sys.stderr.write("[ERROR] --content-only requires --profile or --profile-shapes.\n")
            sys.exit(4)
        profile_shapes_path = safe_path("profiles", args.profile, "shape.ttl")

    for p in [args.content, profile_shapes_path]:
        if not os.path.exists(p):
            sys.stderr.write(f"[ERROR] File not found: {p}\n")
            sys.exit(4)

    try:
        content_graph = load_graph(args.content)
        profile_shapes_graph = load_graph(profile_shapes_path)
    except Exception as e:
        sys.stderr.write(f"[ERROR] {e}\n")
        sys.exit(4)

    content_ok, content_report = run_shacl(content_graph, profile_shapes_graph, "Domain Content")
    print(content_report)

    # Optional cross-check: verify @type matches expected class
    if args.profile:
        full_profile_id = PROFILE_SHORT_NAMES.get(args.profile)
        expected_class = PROFILE_TO_CLASS.get(full_profile_id)
        if expected_class:
            content_types = get_types(content_graph)
            if expected_class not in content_types:
                sys.stderr.write(
                    f"[ERROR] Content @type mismatch: profile '{args.profile}' expects '{expected_class}'.\n"
                    f"        Found @type values: {sorted(content_types)}\n"
                )
                content_ok = False

    if content_ok:
        print("All checks passed.")
        sys.exit(0)
    else:
        print("Content validation failed.")
        sys.exit(2)


def run_full(args):
    """Full validation: wrapper + content + cross-check."""
    wrapper_shapes_path = args.wrapper_shapes
    if args.ids_shapes:
        sys.stderr.write("[WARN] --ids-shapes is deprecated. Use --wrapper-shapes instead.\n")
        wrapper_shapes_path = args.ids_shapes

    for p in [args.wrapper, args.content, wrapper_shapes_path]:
        if not os.path.exists(p):
            sys.stderr.write(f"[ERROR] File not found: {p}\n")
            sys.exit(4)

    try:
        wrapper_graph = load_graph(args.wrapper)
        wrapper_shapes_graph = load_graph(wrapper_shapes_path)
    except Exception as e:
        sys.stderr.write(f"[ERROR] {e}\n")
        sys.exit(4)

    wrapper_ok, wrapper_report = run_shacl(wrapper_graph, wrapper_shapes_graph, "DCAT Wrapper")
    print(wrapper_report)

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

    try:
        content_graph = load_graph(args.content)
        profile_shapes_graph = load_graph(profile_shapes_path)
    except Exception as e:
        sys.stderr.write(f"[ERROR] {e}\n")
        sys.exit(4)

    content_ok, content_report = run_shacl(content_graph, profile_shapes_graph, "Domain Content")
    print(content_report)

    # Cross-check
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
