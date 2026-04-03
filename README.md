# ADV Data Model (AgriDCAT-AP)

**The DCAT Application Profile for agricultural data spaces.**

ADV lets you describe, validate, and govern agricultural datasets for sharing through IDSA/DSP-compliant data spaces. It bridges existing agricultural vocabularies (SOSA, SAREF4AGRI, FOODIE, AGROVOC) with data space governance (DCAT, ODRL) — without reinventing either.

**Version:** 3.0.0 | **License:** [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) | **Namespace:** `https://w3id.org/adv/core#`

---

## What It Does

```
┌─────────────────────────────────────────────────────────────┐
│                    ADV Data Package                         │
│                                                             │
│  ┌───────────────────────┐    ┌───────────────────────────┐ │
│  │  GOVERNANCE WRAPPER   │    │  DOMAIN CONTENT           │ │
│  │  (dcat:Dataset)       │    │  (per profile)            │ │
│  │                       │    │                           │ │
│  │  title, description   │    │  sosa:Observation         │ │
│  │  adv:profileId ───────┼────┼→ saref4agri:Parcel        │ │
│  │  odrl:hasPolicy       │    │  foodie:Intervention      │ │
│  │  dcat:distribution    │    │  saref4agri:Animal        │ │
│  │                       │    │  foodie:Alert             │ │
│  └───────────────────────┘    └───────────────────────────┘ │
│                                                             │
│  SHACL validation on both layers + cross-check              │
└─────────────────────────────────────────────────────────────┘
```

**Two layers, one package:**
1. A **governance wrapper** (DCAT + ODRL) describes your dataset for catalog discovery and attaches usage policies
2. The **domain content** follows an ADV profile that constrains agricultural data using upstream vocabularies

Both layers are validated with SHACL shapes, and a cross-check ensures consistency.

---

## Profiles

| Profile | Target Class | What It Covers |
|---------|-------------|----------------|
| **Observation** | `sosa:Observation` | Sensor or EO measurements (time, value, unit) |
| **Weather Observation** | `sosa:Observation` | Meteorological data (temperature, precipitation, humidity, wind) |
| **Soil Analysis** | `sosa:Observation` | Lab results (pH, nutrients, organic matter, texture) |
| **Parcel-Crop** | `saref4agri:Parcel` | Field boundaries, crop type, area |
| **Intervention** | `foodie:Intervention` | Field operations (spraying, irrigation, harvest) |
| **Animal** | `saref4agri:Animal` | Livestock identification, species, production type |
| **Alert** | `foodie:Alert` | Pest, disease, or weather notifications |

Each profile folder contains:
- `shape.ttl` — SHACL constraints
- `content.template.jsonld` — Fill-in JSON-LD template
- `content.sample.jsonld` — Working example
- `csv-template.csv` — CSV headers with example row

---

## Quick Start

### 1. Pick a profile

Choose the profile that matches your data (e.g., `observation` for sensor readings).

### 2. Fill in the template

Open `profiles/<your-profile>/content.template.jsonld` and replace the placeholders with your data.

### 3. Create the dataset wrapper

Copy `offers/offer.template.jsonld`, fill in the metadata, and pick a policy from `offers/policy-templates/`.

### 4. Validate

```bash
pip install -r validate/requirements.txt

python validate/adv-validate.py \
  --wrapper your-offer.jsonld \
  --content your-data.jsonld
```

Or validate content only (no wrapper needed):

```bash
python validate/adv-validate.py \
  --content your-data.jsonld \
  --content-only --profile observation
```

### 5. Share

Your validated data package is ready for any IDSA connector or DCAT-compatible data space.

---

## Repository Structure

```
model/
  adv-core.ttl              Core ontology (profiles, properties)
  adv-context.jsonld         Shared JSON-LD context
  dsp-wrapper-shapes.ttl     SHACL for DCAT wrapper
  odrl-policy-shapes.ttl     SHACL for ODRL policies
  adv-aim-profile.ttl        AIM vocabulary manifest
  vocabularies/              SKOS concept schemes (severity, sex, productionType)

profiles/
  observation/               Sensor / EO measurements
  weather-observation/       Meteorological data
  soil-analysis/             Soil lab results
  parcel-crop/               Fields and crops
  intervention/              Field operations
  animal/                    Livestock
  alert/                     Notifications

offers/
  offer.template.jsonld      DCAT wrapper template
  offer.sample.jsonld        Working example
  policy-templates/          10 reusable ODRL policies

tests/
  valid/                     Fixtures that should pass validation
  invalid/                   Fixtures that should fail validation
  run-tests.py               Conformance test runner

validate/
  adv-validate.py            Validator (wrapper + content + cross-check)

docs/
  QUICKSTART.md              15-minute tutorial
  VOCABULARY_GUIDE.md        Where to find IRIs for each property
  adapt-alignment.md         ADAPT Standard <-> ADV mapping
  fiware-bridge.md           FIWARE Smart Data Models <-> ADV guide
  translator-alignment.md    NGSI-LD <-> ADV quick mapping
  MIGRATION.md               v2.x -> v3.0 migration guide
  SPARQL.md                  Query patterns

examples/
  observation-soil-moisture/ Complete end-to-end example
```

---

## Policy Templates

ADV includes 10 ready-to-use ODRL policy templates:

| Template | Description |
|----------|-------------|
| `open-access` | Free use with CC BY 4.0 |
| `attribution-required` | Use with mandatory attribution |
| `research-only` | Research purposes only, no redistribution |
| `time-limited` | Access expires after a set date |
| `consortium-only` | Restricted to project consortium members |
| `spatial-restriction` | Limited to a geographic region (e.g., EU only) |
| `advisory-only` | Only for generating farm advisory recommendations |
| `anonymization-required` | Must anonymize before further use |
| `seasonal-access` | Access limited to a growing season window |
| `reciprocal-sharing` | Conditional on sharing equivalent data back |

---

## Upstream Vocabularies

ADV reuses established standards — it does not reinvent them:

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
| Terms | FAO AGROVOC | `http://aims.fao.org/aos/agrovoc/` |

For IRI lookup guidance, see `docs/VOCABULARY_GUIDE.md`.

---

## Interoperability Bridges

ADV connects to the major agricultural data ecosystems:

- **FIWARE / NGSI-LD** — See `docs/fiware-bridge.md` for mapping FIWARE AgriFood entities to ADV profiles
- **ADAPT Standard** — See `docs/adapt-alignment.md` for wrapping precision ag datasets with ADV governance
- **DEMETER AIM** — ADV uses AIM's upstream vocabularies directly (SOSA, SAREF4AGRI, FOODIE)
- **INSPIRE / FOODIE** — Parcel and intervention profiles align with INSPIRE/FOODIE concepts

---

## Contributing

1. Fork this repository
2. Create a new folder under `profiles/` following the existing pattern
3. Add a SHACL shape, JSON-LD template, sample, and CSV template
4. Register the profile in `model/adv-core.ttl` and `model/dsp-wrapper-shapes.ttl`
5. Run validation: `python validate/adv-validate.py --content your-sample.jsonld --content-only --profile your-profile`
6. Run the test suite: `python tests/run-tests.py`
7. Submit a pull request

See `CONTRIBUTING.md` for full guidelines.

---

## License

**Creative Commons Attribution 4.0 International (CC BY 4.0)** — free to share and adapt with attribution.

Developed under **Horizon Europe Grant Agreement 101086461** (AgriDataValue).
