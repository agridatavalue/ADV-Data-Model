#!/usr/bin/env bash
# run-all.sh — Validate all ADV profile samples in one command.
#
# Usage:
#   bash validate/run-all.sh
#
# Requires: pip install rdflib pyshacl
# Exit code: 0 if all pass, 1 if any fail.

set -e
PYTHON="${PYTHON:-python3}"
VALIDATOR="validate/adv-validate.py"
WRAPPER_SHAPES="model/dsp-wrapper-shapes.ttl"

PROFILES=("observation" "parcel-crop" "intervention" "animal" "alert")
PROFILE_IDS=("adv.observation" "adv.parcel-crop" "adv.intervention" "adv.animal" "adv.alert")

FAILURES=0
TOTAL=0

for i in "${!PROFILES[@]}"; do
  PROFILE="${PROFILES[$i]}"
  PID="${PROFILE_IDS[$i]}"
  CONTENT="profiles/${PROFILE}/content.sample.jsonld"

  if [ ! -f "$CONTENT" ]; then
    echo "[SKIP] $CONTENT not found"
    continue
  fi

  # Create a temporary wrapper with the correct profileId
  TMPWRAPPER=$(mktemp /tmp/adv-wrapper-XXXXXX.jsonld)
  cat > "$TMPWRAPPER" <<WRAPPER_EOF
{
  "@context": {
    "dcat": "http://www.w3.org/ns/dcat#",
    "dct": "http://purl.org/dc/terms/",
    "odrl": "http://www.w3.org/ns/odrl/2/",
    "adv": "https://w3id.org/adv/core#",
    "xsd": "http://www.w3.org/2001/XMLSchema#"
  },
  "@id": "https://catalog.example.org/datasets/test-${PROFILE}",
  "@type": "dcat:Dataset",
  "dct:title": "Test dataset for ${PROFILE}",
  "dct:description": "Automated validation test.",
  "dct:identifier": "test-${PROFILE}",
  "adv:profileId": "${PID}",
  "adv:profileVersion": "1.0.0",
  "dct:conformsTo": { "@id": "https://w3id.org/adv/core#${PROFILE}-v1" },
  "dct:license": { "@id": "https://creativecommons.org/licenses/by/4.0/" },
  "dct:issued": { "@value": "2026-01-01T00:00:00Z", "@type": "xsd:dateTime" },
  "dct:publisher": { "@id": "https://example.org/org/test" },
  "dcat:distribution": {
    "@type": "dcat:Distribution",
    "dcat:mediaType": "application/ld+json",
    "dcat:accessURL": { "@id": "https://example.org/data/${PROFILE}" }
  }
}
WRAPPER_EOF

  TOTAL=$((TOTAL + 1))
  echo "--- Validating: ${PROFILE} ---"
  if $PYTHON "$VALIDATOR" --wrapper "$TMPWRAPPER" --content "$CONTENT" 2>&1; then
    echo "[PASS] ${PROFILE}"
  else
    echo "[FAIL] ${PROFILE}"
    FAILURES=$((FAILURES + 1))
  fi
  rm -f "$TMPWRAPPER"
  echo ""
done

echo "========================================="
echo "Results: $((TOTAL - FAILURES))/${TOTAL} passed"
if [ "$FAILURES" -gt 0 ]; then
  echo "FAILED: ${FAILURES} profile(s) did not validate."
  exit 1
else
  echo "All profiles validated successfully."
  exit 0
fi
