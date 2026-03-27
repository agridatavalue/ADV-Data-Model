# ADV Data Model — Release Notes (v1.0.0)

Date: **15 October 2025**  
Maintainer: AgriDataValue Consortium  
License: [CC-BY 4.0](https://creativecommons.org/licenses/by/4.0/)

---

## Overview

Version **1.0.0** of the AgriDataValue (ADV) Data Model introduces a **lean, dataspace-ready architecture** that combines:

- The **AIM ontology** (OGC Agriculture Information Model) for domain semantics.  
- The **ADV layer** for governance, FAIR metadata, and interoperability with IDS and DCAT.  
- A unified **SHACL validation profile** for data quality assurance.  

---

## Highlights

### 1. Simplified Structure

The repository has been completely restructured for clarity and maintainability.

**Old layout (v0.3)**  
- Many small `.ttl` and `.shacl` files (core, dataset, policy, EO, CAP, etc.).  
- Separate `prefixes.ttl` and `index.ttl`.  
- Fragmented documentation.

**New layout (v1.0)**  
- `model/adv.ttl` → single ontology file (AIM + IDS + DCAT + ODRL + EO + CAP).  
- `model/shapes.ttl` → single SHACL profile (core + FAIR + policy).  
- `examples/minimal.ttl` → one clean working example.  
- `docs/SPARQL.md` → consolidated query library.  
- `GETTING_STARTED.md` → beginner-friendly setup guide.  

This design supports long-term scalability and easier onboarding.

---

### 2. Dataspace Alignment

- Integrated **IDS Core** concepts (`ids:Resource`, `ids:ContractOffer`, `ids:Participant`).
- Aligned dataset and service modeling with **DCAT**, **PROV**, and **ODRL**.
- Introduced `adv:hasContract` and `adv:hasRepresentation` for dataspace governance.

Result: **AIM data become FAIR + shareable + governable** within IDS-compliant data spaces.

---

### 3. FAIR Metadata and SHACL Validation

- Consolidated dataset constraints (title, description, publisher, license, distribution).
- Validations for field geometry and observations (property, value, unit, time).
- Added optional SHACL for CAP indicators and EO products.

Result: Every dataset and observation can be validated automatically for FAIR compliance.

---

### 4. Earth Observation and CAP Integration

- `adv:EOProduct` for Sentinel/drone imagery with attributes (tile ID, platform, sensor, cloud cover).  
- `adv:CAPIndicator` for CAP 2023–2027 indicators, linked to `sosa:Observation` via `adv:justifiedBy`.  

These enable **evidence-based policy monitoring** and integration with CAP toolboxes.

---

### 5. Documentation Improvements

- Fully rewritten `README.md` with dataspace explanation and clear structure.  
- Added `GETTING_STARTED.md` for quick adoption.  
- Added `SPARQL.md` for discovery, validation, and governance checks.  
- Markdown-only formatting for clean display on GitLab, GitHub, and portals.

---

## Technical Compatibility

- Fully **backward compatible** with v0.3 classes and properties.  
- SHACL rules and ontology IRIs remain stable (`https://w3id.org/adv#`).  
- Compatible with **AIM 1.0**, **DCAT 3.0**, and **IDS Information Model 4.x**.

---

## Migration Guide (from v0.3)

1. **Replace** all ontology imports with:  
   `model/adv.ttl`  

2. **Replace** all SHACL imports with:  
   `model/shapes.ttl`  

3. **Remove** obsolete modules:  
   - `index.ttl`, `prefixes.ttl`, `policy/`, `alignments/`, `metadata/`, `profiles/`.

4. **Validate your data** using the unified `model/shapes.ttl`.

---

## Next Steps (v1.x Roadmap)

- Controlled vocabularies for CAP indicators and observed properties (SKOS).  
- Deep STAC/DCAT alignment for EO metadata.  
- Advanced ODRL usage control patterns for policy contracts.  
- Integration with **Dataspace Protocol (EDC / Eclipse Dataspace Connector)** self-descriptions.

