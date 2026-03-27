# AgriDataValue (ADV) Data Model
**Version:** 2.0.0
**Date:** 2026-03-27

---

## Overview
The **AgriDataValue (ADV) Data Model** defines a practical and reusable structure for sharing agricultural data across data spaces.
It combines three layers:

1. **AIM-aligned domain semantics** — Uses upstream vocabularies from the AIM stack: W3C SOSA, OGC GeoSPARQL, ETSI SAREF4AGRI, FOODIE/DEMETER
2. **DCAT/DSP governance wrapper** — Dataset self-descriptions using W3C DCAT, aligned with the IDSA Dataspace Protocol
3. **SHACL validation** — Machine-readable constraints for both layers, plus cross-checking

The model provides **five operational profiles** covering the most common data exchange types in AgriDataValue and beyond.

---

## Included Profiles

| Profile | Target Class | Purpose | Example Use Case |
|---------|-------------|---------|------------------|
| **Observation** | `sosa:Observation` | Sensor or Earth Observation measurements (time, value, unit) | Soil moisture, temperature |
| **Parcel-Crop** | `saref4agri:Parcel` | Field and crop descriptions | Field boundaries, crop type |
| **Intervention** | `foodie:Intervention` | Field operations or activities | Spraying, irrigation, fertilisation |
| **Animal** | `saref4agri:Animal` | Livestock and animal information | Animal identification, production events |
| **Alert** | `foodie:Alert` | Notifications and advisories | Pest or disease alerts, weather warnings |

Each profile folder includes:
- A SHACL shape (`shape.ttl`)
- A fill-in JSON-LD template (`content.template.jsonld`)
- A working example (`content.sample.jsonld`)
- A CSV header template (`csv-template.csv`)

---

## Repository Contents

| Folder | Purpose |
|--------|---------|
| **model/** | Core ontology (`adv-core.ttl`), DCAT wrapper shapes (`dsp-wrapper-shapes.ttl`), ODRL policy shapes, JSON-LD context, AIM profile manifest. |
| **offers/** | DCAT dataset self-description templates and ODRL policy templates. |
| **profiles/** | The five operational profiles with SHACL, JSON-LD, and CSV templates. |
| **aim/** | Integration materials for the Agriculture Information Model (AIM). |
| **validate/** | A ready-to-use validator script (`adv-validate.py`) that checks data files. |
| **registry/** | FAIR-style metadata registry describing each artifact. |
| **w3id/** | Instructions for permanent namespace setup under `https://w3id.org/adv/`. |
| **docs/** | Analysis, development plan, migration guide, SPARQL queries, and alignment notes. |

---

## Using the ADV Model

### Step 1 — Choose Your Profile
Select the profile that fits your data (for example, **observation** if you have sensor readings).

### Step 2 — Prepare Your Data
Open the JSON-LD template in the chosen profile folder.
Replace the placeholder values with your real data.
You can also fill in the CSV template and convert it to JSON-LD using simple scripts.

### Step 3 — Describe the Dataset
Duplicate `offers/offer.template.jsonld`, fill the metadata fields (`dct:title`, `dct:description`, `adv:profileId`, `adv:profileVersion`, etc.), and select a usage policy from `offers/policy-templates/`.

### Step 4 — Validate
Run the included validator to make sure both files conform:

```
python validate/adv-validate.py \
  --wrapper offers/offer.sample.jsonld \
  --content profiles/observation/content.sample.jsonld
```

The script:
- Checks the DCAT wrapper against `model/dsp-wrapper-shapes.ttl`
- Checks the domain content against the relevant SHACL shape
- Verifies that the declared `adv:profileId` matches the actual class used in the content

### Step 5 — Publish or Exchange
Once validation passes, your data package is **ADV-compliant** and ready to be shared through an IDSA connector or any DCAT-compatible data space environment.

---

## Upstream Vocabulary Alignment

ADV v2.0 uses the **actual upstream URIs** from the AIM vocabulary stack:

| Domain | Vocabulary | Namespace |
|--------|-----------|-----------|
| Observations | W3C SOSA | `http://www.w3.org/ns/sosa/` |
| Geometry | OGC GeoSPARQL | `http://www.opengis.net/ont/geosparql#` |
| Agriculture | ETSI SAREF4AGRI | `https://saref.etsi.org/saref4agri/` |
| Agriculture | FOODIE/DEMETER | `http://foodie-cloud.com/model/foodie#` |
| Quantities | QUDT | `http://qudt.org/schema/qudt/` |
| Provenance | W3C PROV | `http://www.w3.org/ns/prov#` |
| Governance | W3C DCAT | `http://www.w3.org/ns/dcat#` |
| Policies | W3C ODRL | `http://www.w3.org/ns/odrl/2/` |

A shared JSON-LD context file is available at `model/adv-context.jsonld`.

For detailed term usage, see `aim/aim-quick-reference.md`.

---

## Validation and Interoperability

Validation is performed with **SHACL** rules to guarantee consistent data structures across pilots.
This ensures:
- Data discoverability and usability in DCAT/DSP-based data spaces.
- Interoperability between applications using the same profiles.
- Easier extension with local properties without breaking compatibility.

---

## FAIR and Reuse

Each artifact is documented in `registry/artifacts-metadata.json` with:
- version, path, and license
- last update date
- file format

All assets are licensed under **Creative Commons Attribution 4.0 International (CC BY 4.0)**.

---

## Why Only Five Profiles

These profiles were selected to cover 90% of data types across the AgriDataValue pilots.
They can be easily extended if new scenarios arise (for example, market data or EO scenes) following the same design pattern.

---

## How to Extend or Contribute

1. Create a new folder under `profiles/` following the same structure.
2. Add a SHACL shape, JSON-LD template, and sample file.
3. Register the new profile in `model/adv-core.ttl`.
4. Validate it with the existing script before submitting.

See `CONTRIBUTING.md` for full contribution guidelines.

---

## Migrating from v1.x

Version 2.0 introduces breaking namespace changes. See `docs/MIGRATION.md` for a complete mapping table and step-by-step migration guide.

---

## License

This project is licensed under **Creative Commons Attribution 4.0 International (CC BY 4.0)**.
You are free to share and adapt the model as long as proper credit is given.

---

**AgriDataValue Data Model**
Developed under Horizon Europe Grant Agreement 101086461
