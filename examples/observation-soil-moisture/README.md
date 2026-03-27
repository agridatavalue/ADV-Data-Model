# End-to-End Example: Soil Moisture Observation

This directory shows a **complete ADV data package** for a soil moisture observation, including all three layers.

## Scenario

A soil moisture sensor (SM-10) in Field A records volumetric water content at 10 cm depth every 10 minutes. The data provider wants to publish the September 2025 time series in an agricultural data space with open access.

## Files

| File | Layer | Purpose |
|------|-------|---------|
| `content.jsonld` | Domain content | The observation payload (sosa:Observation with QUDT result) |
| `offer.jsonld` | Governance wrapper | DCAT dataset self-description with ADV profile reference |
| `policy.jsonld` | Usage policy | ODRL open-access policy (CC BY 4.0) |

## How the Layers Fit Together

```
offer.jsonld (dcat:Dataset)
  ├── adv:profileId = "adv.observation"    ← links to ADV profile
  ├── dcat:distribution                     ← how to access the data
  ├── odrl:hasPolicy → policy.jsonld        ← usage conditions
  └── validates against: model/dsp-wrapper-shapes.ttl

content.jsonld (sosa:Observation)
  ├── sosa:resultTime, sosa:observedProperty, etc.
  └── validates against: profiles/observation/shape.ttl

Cross-check: offer's profileId "adv.observation"
             must match content's @type "sosa:Observation"
```

## Validate

From the repository root:

```bash
python validate/adv-validate.py \
  --wrapper examples/observation-soil-moisture/offer.jsonld \
  --content examples/observation-soil-moisture/content.jsonld
```

Expected output:
```
=== Validation Report: DCAT Wrapper ===
Validation Report
Conforms: True

=== Validation Report: Domain Content ===
Validation Report
Conforms: True

All checks passed.
```

## Raw Data (Before Transformation)

A typical raw CSV from a sensor platform might look like:

```csv
timestamp,sensor_id,field_id,parameter,value,unit
2025-09-21T10:35:00Z,SM-10,field-a,soil_moisture,0.23,m3/m3
```

To produce `content.jsonld`, you would:
1. Map `parameter` → `sosa:observedProperty` IRI (e.g., from QUDT or AGROVOC)
2. Map `value` + `unit` → `sosa:hasResult` with `qudt:numericValue` and `qudt:unit`
3. Map `timestamp` → `sosa:resultTime`
4. Map `sensor_id` → `sosa:madeBySensor` IRI
5. Map `field_id` → `sosa:hasFeatureOfInterest` IRI
