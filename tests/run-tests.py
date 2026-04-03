#!/usr/bin/env python3
"""
ADV Conformance Test Suite

Runs all test fixtures in tests/valid/ and tests/invalid/ against
the appropriate SHACL shapes and reports pass/fail results.

Usage:
  python tests/run-tests.py

Exit codes:
  0 = All tests passed (valid fixtures conform, invalid fixtures fail)
  1 = One or more tests produced unexpected results
"""

import os
import sys
from pathlib import Path

# Add parent directory to path so we can import the validator helpers
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from rdflib import Graph, Namespace
from rdflib.namespace import RDF

try:
    from pyshacl import validate as shacl_validate
except ImportError:
    sys.stderr.write("[ERROR] pyshacl is required. Install with: pip install pyshacl\n")
    sys.exit(1)

ROOT = Path(__file__).resolve().parent.parent
ADV = Namespace("https://w3id.org/adv/core#")

# Map content @type to profile shape file
TYPE_TO_SHAPE = {
    "http://www.w3.org/ns/sosa/Observation": "profiles/observation/shape.ttl",
    "https://saref.etsi.org/saref4agri/Parcel": "profiles/parcel-crop/shape.ttl",
    "http://foodie-cloud.com/model/foodie#Intervention": "profiles/intervention/shape.ttl",
    "https://saref.etsi.org/saref4agri/Animal": "profiles/animal/shape.ttl",
    "http://foodie-cloud.com/model/foodie#Alert": "profiles/alert/shape.ttl",
    "http://www.w3.org/ns/dcat#Dataset": "model/dsp-wrapper-shapes.ttl",
}

WRAPPER_SHAPES = ROOT / "model" / "dsp-wrapper-shapes.ttl"


def load_graph(path):
    g = Graph()
    ext = str(path).lower().split(".")[-1]
    fmt = "json-ld" if ext in ("jsonld", "json") else "turtle"
    g.parse(str(path), format=fmt)
    return g


def get_types(g):
    return {str(o) for _, _, o in g.triples((None, RDF.type, None))}


def find_shape(types):
    for t in types:
        if t in TYPE_TO_SHAPE:
            return ROOT / TYPE_TO_SHAPE[t]
    return None


def run_shacl(data_graph, shapes_path):
    shapes_graph = Graph()
    shapes_graph.parse(str(shapes_path), format="turtle")
    conforms, _, results_text = shacl_validate(
        data_graph=data_graph,
        shacl_graph=shapes_graph,
        inference="rdfs",
        allow_infos=True,
        allow_warnings=True,
    )
    return conforms, results_text.strip()


def main():
    valid_dir = ROOT / "tests" / "valid"
    invalid_dir = ROOT / "tests" / "invalid"

    passed = 0
    failed = 0
    errors = []

    print("=" * 60)
    print("ADV Conformance Test Suite")
    print("=" * 60)

    # Test valid fixtures (should all pass)
    print("\n--- Valid fixtures (expecting PASS) ---\n")
    for f in sorted(valid_dir.glob("*.jsonld")):
        try:
            g = load_graph(f)
            types = get_types(g)
            shape_path = find_shape(types)
            if not shape_path:
                print(f"  SKIP  {f.name} (no matching shape for types: {types})")
                continue
            conforms, report = run_shacl(g, shape_path)
            if conforms:
                print(f"  PASS  {f.name}")
                passed += 1
            else:
                print(f"  FAIL  {f.name} (expected PASS but got validation errors)")
                errors.append(f"VALID/{f.name}: expected PASS\n{report}")
                failed += 1
        except Exception as e:
            print(f"  ERROR {f.name}: {e}")
            errors.append(f"VALID/{f.name}: {e}")
            failed += 1

    # Test invalid fixtures (should all fail validation)
    print("\n--- Invalid fixtures (expecting FAIL) ---\n")
    for f in sorted(invalid_dir.glob("*.jsonld")):
        try:
            g = load_graph(f)
            types = get_types(g)
            shape_path = find_shape(types)
            if not shape_path:
                print(f"  SKIP  {f.name} (no matching shape for types: {types})")
                continue
            conforms, report = run_shacl(g, shape_path)
            if not conforms:
                print(f"  PASS  {f.name} (correctly rejected)")
                passed += 1
            else:
                print(f"  FAIL  {f.name} (expected FAIL but validation passed)")
                errors.append(f"INVALID/{f.name}: expected FAIL but passed")
                failed += 1
        except Exception as e:
            print(f"  ERROR {f.name}: {e}")
            errors.append(f"INVALID/{f.name}: {e}")
            failed += 1

    # Summary
    print(f"\n{'=' * 60}")
    print(f"Results: {passed} passed, {failed} failed")
    print(f"{'=' * 60}")

    if errors:
        print("\nDetails of failures:")
        for err in errors:
            print(f"\n  {err}")

    sys.exit(0 if failed == 0 else 1)


if __name__ == "__main__":
    main()
