# CHANGELOG
All notable changes to this project will be documented in this file.  
This project adheres to **Semantic Versioning (SEMVER)**.

---

## [Unreleased]
### Planned
- Add more examples based on pilot feedback.
- Extend mappings with any newly adopted AIM modules.
- Add extended SHACL result examples and FAIR metadata descriptors.
- Provide JSON Schema equivalents for lightweight validation.
- Prepare W3ID redirection setup for public namespace resolution.
- Release documentation for integration with data-model translators.
- Provide Docker container for validation and local testing.

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

## [1.0.0 – Archive Reference from 2025-10-15]
### Added (Historical Context)
- Original prototype with:
  - `model/adv.ttl` — combined RDF vocabulary (core + operations + sensing + assets).
  - `model/adv.context.jsonld` — single JSON-LD context for all profiles.
  - Profiles under `core/`, `operations/`, `sensing/`, and `assets/`.
- Minimal examples, AIM/IDS mappings, and documentation pages (overview, entities, interop guides).

---

[Unreleased]: #
[1.1.0]: #
[1.0.0]: #
