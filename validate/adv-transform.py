#!/usr/bin/env python3
"""
adv-transform.py — CSV to ADV JSON-LD transformer

Reads a CSV file matching an ADV profile template and produces valid
JSON-LD content files that pass SHACL validation.

Usage:
  # Transform a CSV to JSON-LD (one file per row, or one array):
  python validate/adv-transform.py \\
    --profile observation \\
    --input my-data.csv \\
    --output my-data.jsonld

  # Use --base-uri to set the IRI prefix for generated entities:
  python validate/adv-transform.py \\
    --profile observation \\
    --input my-data.csv \\
    --output my-data.jsonld \\
    --base-uri https://data.my-org.org/

Supported profiles: observation, parcel-crop, intervention, animal, alert

The CSV must use the column headers from profiles/<profile>/csv-template.csv.
"""

import argparse
import csv
import json
import sys
from pathlib import Path


# ---------- Profile-specific transformers ----------

def transform_observation(row, base):
    eid = row["externalId"]
    return {
        "@context": OBSERVATION_CONTEXT,
        "@id": f"{base}observation/{eid}",
        "@type": "sosa:Observation",
        "sosa:resultTime": typed_dt(row["resultTime"]),
        "sosa:observedProperty": iri(row["observedProperty"]),
        "sosa:madeBySensor": {"@id": row["madeBySensor"], "@type": "sosa:Sensor"},
        "sosa:hasFeatureOfInterest": {"@id": row["featureOfInterest"], "@type": "sosa:FeatureOfInterest"},
        "sosa:hasResult": {
            "qudt:numericValue": typed_dec(row["value"]),
            "qudt:unit": iri(row["unit"]),
        },
        "adv:externalId": eid,
        **optional_dt("adv:issuedAt", row.get("issuedAt")),
    }

def transform_parcel_crop(row, base):
    eid = row["externalId"]
    geom_coords = row["geometryCoordinatesWGS84"]
    try:
        coords = json.loads(geom_coords)
    except json.JSONDecodeError:
        coords = geom_coords

    doc = {
        "@context": PARCEL_CROP_CONTEXT,
        "@id": f"{base}parcel/{eid}",
        "@type": "saref4agri:Parcel",
        "adv:externalId": eid,
        "geo:hasGeometry": {
            "@id": f"{base}geometry/{eid}",
            "@type": f"geojson:{row['geometryType']}",
            "geojson:coordinates": coords,
            "geojson:crs": "EPSG:4326",
        },
        "saref4agri:hasCrop": {
            "@id": f"{base}crop/{row['cropInstanceId']}",
            "@type": "saref4agri:Crop",
            "foodie:cropSpecies": iri(row["cropSpeciesIRI"]),
        },
    }
    if row.get("cropArea"):
        doc["foodie:cropArea"] = typed_dec(row["cropArea"])
    if row.get("issuedAt"):
        doc.update(optional_dt("adv:issuedAt", row["issuedAt"]))
    return doc

def transform_intervention(row, base):
    eid = row["externalId"]
    doc = {
        "@context": INTERVENTION_CONTEXT,
        "@id": f"{base}intervention/{eid}",
        "@type": "foodie:Intervention",
        "adv:externalId": eid,
        "dct:type": iri(row["typeIRI"]),
        "prov:startedAtTime": typed_dt(row["startedAtTime"]),
        "prov:endedAtTime": typed_dt(row["endedAtTime"]),
        "sosa:hasFeatureOfInterest": {"@id": row["featureOfInterest"], "@type": "sosa:FeatureOfInterest"},
    }
    if row.get("usedId"):
        doc["prov:used"] = {
            "@id": row["usedId"],
            "@type": "schema:Product",
            "qudt:numericValue": typed_dec(row["usedQuantity"]),
            "qudt:unit": iri(row["usedUnitIRI"]),
        }
    if row.get("generatedId"):
        doc["prov:generated"] = {
            "@id": row["generatedId"],
            "@type": "schema:Product",
            "qudt:numericValue": typed_dec(row["generatedQuantity"]),
            "qudt:unit": iri(row["generatedUnitIRI"]),
        }
    if row.get("issuedAt"):
        doc.update(optional_dt("adv:issuedAt", row["issuedAt"]))
    return doc

def transform_animal(row, base):
    eid = row["externalId"]
    doc = {
        "@context": ANIMAL_CONTEXT,
        "@id": f"{base}animal/{eid}",
        "@type": "saref4agri:Animal",
        "adv:externalId": eid,
        "adv:species": iri(row["speciesIRI"]),
        "adv:birthDate": typed_date(row["birthDate"]),
    }
    if row.get("sexIRI"):
        doc["adv:sex"] = iri(row["sexIRI"])
    if row.get("productionTypeIRI"):
        doc["adv:productionType"] = iri(row["productionTypeIRI"])
    if row.get("parentId"):
        doc["adv:hasParent"] = iri(row["parentId"])
    if row.get("issuedAt"):
        doc.update(optional_dt("adv:issuedAt", row["issuedAt"]))
    return doc

def transform_alert(row, base):
    eid = row["externalId"]
    doc = {
        "@context": ALERT_CONTEXT,
        "@id": f"{base}alert/{eid}",
        "@type": "foodie:Alert",
        "adv:externalId": eid,
        "dct:type": iri(row["typeIRI"]),
        "adv:severity": iri(row["severityIRI"]),
        "dct:description": row["description"],
        "sosa:hasFeatureOfInterest": {"@id": row["featureOfInterest"], "@type": "sosa:FeatureOfInterest"},
    }
    if row.get("startedAtTime"):
        doc["prov:startedAtTime"] = typed_dt(row["startedAtTime"])
    if row.get("endedAtTime"):
        doc["prov:endedAtTime"] = typed_dt(row["endedAtTime"])
    if row.get("issuedAt"):
        doc.update(optional_dt("adv:issuedAt", row["issuedAt"]))
    return doc


# ---------- Helpers ----------

def iri(val):
    return {"@id": val}

def typed_dt(val):
    return {"@value": val, "@type": "xsd:dateTime"}

def typed_dec(val):
    return {"@value": str(val), "@type": "xsd:decimal"}

def typed_date(val):
    return {"@value": val, "@type": "xsd:date"}

def optional_dt(key, val):
    if val:
        return {key: typed_dt(val)}
    return {}


# ---------- Contexts ----------

OBSERVATION_CONTEXT = {
    "sosa": "http://www.w3.org/ns/sosa/",
    "qudt": "http://qudt.org/schema/qudt/",
    "adv": "https://w3id.org/adv/core#",
    "xsd": "http://www.w3.org/2001/XMLSchema#",
    "unit": "http://qudt.org/vocab/unit/",
}

PARCEL_CROP_CONTEXT = {
    "saref4agri": "https://saref.etsi.org/saref4agri/",
    "geo": "http://www.opengis.net/ont/geosparql#",
    "foodie": "http://foodie-cloud.com/model/foodie#",
    "adv": "https://w3id.org/adv/core#",
    "xsd": "http://www.w3.org/2001/XMLSchema#",
    "geojson": "https://purl.org/geojson/vocab#",
}

INTERVENTION_CONTEXT = {
    "foodie": "http://foodie-cloud.com/model/foodie#",
    "sosa": "http://www.w3.org/ns/sosa/",
    "prov": "http://www.w3.org/ns/prov#",
    "dct": "http://purl.org/dc/terms/",
    "qudt": "http://qudt.org/schema/qudt/",
    "adv": "https://w3id.org/adv/core#",
    "xsd": "http://www.w3.org/2001/XMLSchema#",
    "unit": "http://qudt.org/vocab/unit/",
    "schema": "https://schema.org/",
}

ANIMAL_CONTEXT = {
    "saref4agri": "https://saref.etsi.org/saref4agri/",
    "adv": "https://w3id.org/adv/core#",
    "xsd": "http://www.w3.org/2001/XMLSchema#",
}

ALERT_CONTEXT = {
    "foodie": "http://foodie-cloud.com/model/foodie#",
    "sosa": "http://www.w3.org/ns/sosa/",
    "prov": "http://www.w3.org/ns/prov#",
    "dct": "http://purl.org/dc/terms/",
    "adv": "https://w3id.org/adv/core#",
    "xsd": "http://www.w3.org/2001/XMLSchema#",
}

TRANSFORMERS = {
    "observation": transform_observation,
    "parcel-crop": transform_parcel_crop,
    "intervention": transform_intervention,
    "animal": transform_animal,
    "alert": transform_alert,
}


# ---------- Main ----------

def main():
    parser = argparse.ArgumentParser(
        description="Transform ADV CSV files to valid JSON-LD."
    )
    parser.add_argument("--profile", required=True,
                        choices=list(TRANSFORMERS.keys()),
                        help="ADV profile name.")
    parser.add_argument("--input", required=True,
                        help="Path to input CSV file.")
    parser.add_argument("--output", default=None,
                        help="Path to output JSON-LD file. Default: stdout.")
    parser.add_argument("--base-uri", default="https://data.example.org/",
                        help="Base URI for generated entity IRIs.")
    args = parser.parse_args()

    if not Path(args.input).exists():
        sys.stderr.write(f"[ERROR] File not found: {args.input}\n")
        sys.exit(1)

    transformer = TRANSFORMERS[args.profile]
    base = args.base_uri.rstrip("/") + "/"

    results = []
    with open(args.input, newline="", encoding="utf-8") as f:
        # Skip comment lines and blank lines
        lines = [line for line in f if not line.startswith("#") and line.strip()]

    reader = csv.DictReader(lines)
    for row in reader:
        # Strip whitespace from keys and values
        row = {k.strip(): v.strip() for k, v in row.items() if k}
        try:
            doc = transformer(row, base)
            results.append(doc)
        except KeyError as e:
            sys.stderr.write(f"[ERROR] Missing column {e} in row: {row}\n")
            sys.exit(1)

    if len(results) == 0:
        sys.stderr.write("[ERROR] No data rows found in CSV.\n")
        sys.exit(1)

    # Output single object if one row, array if multiple
    output = results[0] if len(results) == 1 else results

    out_str = json.dumps(output, indent=2, ensure_ascii=False)

    if args.output:
        Path(args.output).write_text(out_str + "\n", encoding="utf-8")
        sys.stderr.write(f"[OK] Wrote {len(results)} record(s) to {args.output}\n")
    else:
        print(out_str)


if __name__ == "__main__":
    main()
