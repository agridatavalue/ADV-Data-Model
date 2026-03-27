# CHANGELOG
All notable changes to this project will be documented in this file.
This project adheres to **Semantic Versioning (SEMVER)**.

---

## [Unreleased]
### Planned
- Add more examples based on pilot feedback.
- Provide JSON Schema equivalents for lightweight validation.
- Build CI/CD validation pipeline (GitHub Actions).
- Collect real pilot data examples from SYN toolbox.
- Prepare W3ID redirection setup for public namespace resolution.
- Provide Docker container for validation and local testing.

---

## [2.0.0] – 2026-03-27
### Breaking Changes
- **AIM namespace realignment** — All `aim:*` references (`https://w3id.org/aim#`) replaced with actual upstream vocabulary URIs:
  - `aim:Observation` → `sosa:Observation` (W3C SOSA)
  - `aim:FeatureOfInterest` → `sosa:FeatureOfInterest` or `saref4agri:Parcel` (SAREF4AGRI)
  - `aim:Activity` → `foodie:Intervention` (FOODIE/DEMETER)
  - `aim:Animal` → `saref4agri:Animal` (SAREF4AGRI)
  - `aim:Alert` → `foodie:Alert` (FOODIE/DEMETER)
  - All properties updated to use SOSA, GeoSPARQL, QUDT, PROV, Dublin Core, Schema.org URIs.
  - See `docs/MIGRATION.md` for the complete mapping table.

- **Wrapper migration from IDS to DCAT** — `ids:Resource` replaced with `dcat:Dataset`, aligned with the IDSA Dataspace Protocol (DSP):
  - `ids:representation` → `dcat:distribution`
  - Added `dct:conformsTo` for profile URI reference.
  - Added `odrl:hasPolicy` for usage control.

### Added
- **`model/dsp-wrapper-shapes.ttl`** — New DCAT-based wrapper SHACL shapes (replaces `ids-wrapper-shapes.ttl`).
- **`model/odrl-policy-shapes.ttl`** — Minimal SHACL for validating ODRL policies.
- **`model/adv-context.jsonld`** — Shared JSON-LD context file for all ADV terms and upstream prefixes.
- **`model/adv-aim-profile.ttl`** — Manifest documenting which upstream terms each ADV profile uses.
- **`offers/policy-templates/`** — Four ODRL policy patterns:
  - `open-access.jsonld` — CC BY 4.0, no restrictions.
  - `research-only.jsonld` — Research purpose only, redistribution prohibited.
  - `attribution-required.jsonld` — Must credit the provider.
  - `time-limited.jsonld` — Access expires after a defined date.
- **`docs/MIGRATION.md`** — Complete migration guide from v1.x to v2.0 with mapping tables.

### Changed
- **`model/adv-core.ttl`** — Updated to v2.0.0; profile `appliesTo` targets now reference real upstream classes.
- **All 5 profile SHACL shapes** — Property paths updated to use SOSA, GeoSPARQL, SAREF4AGRI, FOODIE, PROV, Dublin Core URIs.
- **All 10 JSON-LD templates and samples** — `@context` blocks and property names updated to match new SHACL.
- **`offers/offer.template.jsonld` and `offer.sample.jsonld`** — Migrated from `ids:Resource` to `dcat:Dataset`; added distribution and policy blocks.
- **`validate/adv-validate.py`** — Updated to validate DCAT wrapper; cross-checks against correct upstream class URIs; new `--wrapper-shapes` flag (legacy `--ids-shapes` deprecated); fixed default path.
- **`aim/aim-quick-reference.md`** — Rewritten with actual upstream vocabulary URIs and namespace tables.
- **`aim/pinned-import.ttl`** — Points to actual DEMETER/AIM ontology URI and individual upstream standards.
- **`docs/translator-alignment.md`** — Updated property mappings for new namespaces.
- **`docs/SPARQL.md`** — Updated prefix block and queries for DCAT-based wrapper.
- **`CONTRIBUTING.md`** — Updated validation instructions for new wrapper shapes.
- **README.md** — Rewritten for v2.0 with upstream vocabulary alignment section.

### Compliance
- Fully aligns with Grant Agreement 101086461 (AgriDataValue) and Deliverables **D1.3**, **D1.4**, **D3.1–D3.5**.
- Domain content now validates against real AIM-compliant data produced by the toolbox (SOSA/GeoSPARQL URIs).
- Wrapper is compatible with IDSA Dataspace Protocol DCAT catalog.

---

## [1.1.0] – 2025-10-31
### Added
- **AIM Integration Layer** (`aim/` folder)
  - `aim-quick-reference.md`: concise documentation of AIM classes and properties used by ADV.
  - `pinned-import.ttl`: minimal file importing the official AIM ontology.
- **Improved README** for clear onboarding, describing repository structure, profiles, and AIM usage.
- **FAIR metadata registry** (`registry/artifacts-metadata.json`) listing key artifacts.
- **W3ID folder** with redirect setup guide for stable namespace publishing.
- **Updated validator (`validate/adv-validate.py`)**
  - Adds cross-check between `adv:profileId` and AIM content `@type`.
  - Ensures wrapper/content consistency in addition to SHACL validation.
- **Updated offer template** with optional `ids:representation` and `ids:defaultEndpoint` placeholders.
- **Parcel-Crop profile fix**: corrected filename `content.template-jsonld` → `content.template.jsonld`.
- **Translator alignment guide** (`docs/translator-alignment.md`) mapping NGSI-LD fields to ADV profiles.

### Improved
- Simplified repository layout for clarity: profiles, model, offers, validate, aim, registry.
- README rewritten for non-experts: 5-step usage guide, AIM section, and FAIR compliance summary.
- Validation and cross-checking logic fully aligned with Task 1.3 interoperability principles.
- Profiles, examples, and CSV templates made consistent across all folders.

### Compliance
- Fully aligns with Grant Agreement 101086461 (AgriDataValue) and Deliverables **D1.3**, **D1.4**, **D3.1–D3.5**.
- Implements recommendations from **Task 1.3 – Semantic Interoperability Guidelines** and **AIM v2025.10** release.
- Ready for pilot deployment and external reuse by other projects.

---

## [1.0.0] – 2025-10-30
### Added
- **Repository structure finalized** with core model, profiles, offers, and validation tool.
- Introduced **ADV Core Ontology** (`model/adv-core.ttl`) for profile identification and versioning.
- Added **SHACL validation for IDS offers** (`model/ids-wrapper-shapes.ttl`).
- Implemented **five operational profiles** aligned with project deliverables:
  - **Observation** — sensor & EO measurements
  - **Parcel-Crop** — parcels, fields, and crop instances
  - **Intervention** — field operations
  - **Animal** — livestock and animal data
  - **Alert** — pest, disease, and advisory notifications
- Provided **template and sample JSON-LD files** for all profiles.
- Added **simple validator** (`validate/adv-validate.py`) for IDS and AIM layers.
- Packaged the model as a **ready-to-deploy, pilot-ready product**.

### Compliance
This release fulfills the functional and structural requirements defined in:
- Grant Agreement 101086461 (AgriDataValue)
- Deliverables **D1.3**, **D1.4**, **D3.1–D3.5**
- **Task 1.3 Semantic Interoperability Guidelines**

### Notes
- This release replaces the earlier experimental version (`model/adv.ttl`, `model/adv.context.jsonld`, and separated domain folders).
- The new structure simplifies onboarding, keeps the RDF backbone consistent, and enables direct pilot use.

---

[Unreleased]: #
[2.0.0]: #
[1.1.0]: #
[1.0.0]: #
