# ADV Data Model — Improvement Analysis

**Date:** 2026-03-27
**Author:** IDSA / Task 1.3
**Version:** Draft for internal review

---

## 1. Current State Assessment

### 1.1 What Exists (Inventory)

The ADV Data Model repository (v1.1.0, dated 2025-10-31) contains **34 files** across a well-organized structure:

| Category | Count | Files |
|----------|-------|-------|
| Core ontology | 1 | `model/adv-core.ttl` — defines `adv:Profile` class, 5 profile instances, 3 cross-cutting properties |
| IDS wrapper SHACL | 1 | `model/ids-wrapper-shapes.ttl` — validates `ids:Resource` offers |
| Profile SHACL shapes | 5 | One per profile (observation, parcel-crop, intervention, animal, alert) |
| JSON-LD templates | 5 | Editable templates with `REPLACE_*` placeholders |
| JSON-LD examples | 5 | Working sample payloads |
| IDS offer template + example | 2 | `offers/offer.template.jsonld`, `offers/offer.sample.jsonld` |
| CSV templates | 5 | One per profile — tabular alternative for non-RDF producers |
| Validation script | 1 | `validate/adv-validate.py` (Python, rdflib + pyshacl) |
| AIM integration | 2 | `aim/aim-quick-reference.md`, `aim/pinned-import.ttl` |
| Metadata registry | 1 | `registry/artifacts-metadata-json` |
| Documentation | 6 | README, CHANGELOG, CONTRIBUTING, SPARQL queries, translator alignment, release notes |

**Verdict:** The repository is structurally sound and more complete than what D1.4 promised. The five profiles exist as machine-readable artefacts with SHACL shapes, templates, examples, and a working validator. This is a solid foundation.

### 1.2 What Works

1. **Profile-driven architecture** — The separation of "IDS wrapper" (discovery/governance) from "AIM content" (domain semantics) is clean and well-implemented. Each profile is self-contained.

2. **SHACL validation** — Both the wrapper shapes (`ids-wrapper-shapes.ttl`) and profile-specific content shapes are functional. The validator script performs three checks: wrapper conformance, content conformance, and wrapper↔content cross-check.

3. **Developer experience** — The 5-step usage guide in README.md, the JSON-LD templates with placeholders, CSV templates for tabular producers, and the `aim-quick-reference.md` make onboarding realistic for pilot developers.

4. **Extensibility pattern** — `CONTRIBUTING.md` documents how to add a 6th profile. The `adv-core.ttl` ontology is designed for this.

5. **FAIR metadata** — The registry file, CC BY 4.0 licensing, and semantic versioning are in place.

### 1.3 What's Missing or Problematic

The following issues range from critical (blocks interoperability) to strategic (blocks industry adoption).

---

## 2. Semantic Issues

### 2.1 CRITICAL: AIM Namespace Mismatch

**This is the single most important issue in the repository.**

The ADV model uses namespace `https://w3id.org/aim#` throughout — in the core ontology, all SHACL shapes, all JSON-LD templates/examples, and the validator. For example:

```turtle
# ADV references:
aim:Observation    # https://w3id.org/aim#Observation
aim:FeatureOfInterest
aim:Activity
aim:Animal
aim:Alert
aim:resultTime
aim:hasGeometry
aim:hasCrop
```

However, the **actual AIM OGC SWG repository** (https://github.com/opengeospatial/aim-swg) uses completely different namespaces:

| ADV references | Actual AIM (OGC SWG) |
|---|---|
| `aim:Observation` | `sosa:Observation` (W3C SOSA, `http://www.w3.org/ns/sosa/`) |
| `aim:FeatureOfInterest` | `sosa:FeatureOfInterest` |
| `aim:resultTime` | `sosa:resultTime` |
| `aim:madeBySensor` | `sosa:madeBySensor` |
| `aim:hasResult` | `sosa:hasResult` |
| `aim:hasGeometry` | `geo:hasGeometry` (GeoSPARQL, `http://www.opengis.net/ont/geosparql#`) |
| `aim:Animal` | `saref4agri:Animal` (ETSI SAREF4AGRI, `https://saref.etsi.org/saref4agri/`) |
| `aim:hasCrop` | `saref4agri:hasCrop` or `fiware-agrifood:AgriCrop` |
| `aim:Alert` | Defined in `https://w3id.org/demeter/agri/agriAlert` module |

The AIM ontology has `@base <https://w3id.org/demeter/>` and module URIs like `https://w3id.org/demeter/agri/agriFeature`. It does **not** define a `https://w3id.org/aim#` namespace.

**Impact:**
- **No instance of ADV would validate against the real AIM** if a consumer tried to use both vocabularies together.
- The SHACL shapes target classes (`aim:Observation`) that don't match the URIs in real AIM-compliant data.
- The toolbox (D3.2/D3.5) uses the DEMETER context (`https://w3id.org/demeter/agri-context.jsonld`) which maps to SOSA/GeoSPARQL URIs, not `aim:*`.

**Root cause:** The `aim-quick-reference.md` states "AIM v2025.10 (October release), namespace root `https://w3id.org/aim#`" — suggesting the ADV model was designed against an anticipated future AIM version with a unified namespace. However, the current AIM SWG repository (v3.0, March 2023) does not use this namespace, and there is no public evidence that this namespace migration has been implemented.

**Resolution options:**
- **Option A (recommended)**: Align ADV with the actual AIM/DEMETER namespaces. Use `sosa:Observation`, `geo:hasGeometry`, etc. directly, and use the `demeter-core-context.jsonld` from AIM as the base context.
- **Option B**: If the OGC AIM SWG has committed to the `https://w3id.org/aim#` namespace in a forthcoming release, document this dependency explicitly and provide a compatibility layer that maps between the current DEMETER URIs and the future AIM URIs.
- **Option C**: Define `https://w3id.org/aim#` as an ADV-managed alias namespace with explicit `owl:equivalentClass` / `owl:equivalentProperty` mappings to the actual SOSA/GeoSPARQL/SAREF4AGRI terms. This is technically valid but adds maintenance burden.

### 2.2 Legacy D1.3 Mapping Tables Not Formally Deprecated

The D1.4 deliverable explicitly abandoned the one-to-one class mappings from D1.3 (e.g., `AgriPest ↔ Alert`, `CropType ↔ Resource`). However, the repository contains no explicit deprecation notice. If someone reads D1.3 (a published deliverable) and comes to this repo, there is nothing telling them those mappings are superseded.

**Impact:** Confusion for new integrators who may find D1.3 first.

**Resolution:** Add a `docs/MIGRATION.md` document that explicitly states: "The class-to-class mapping tables from D1.3 (Tables 7, 8, 9) are deprecated. ADV now uses a profile-driven approach where AIM provides domain semantics and IDS/DCAT provides the governance wrapper."

### 2.3 IDS Namespace Alignment

The IDS wrapper shapes use `ids: <https://w3id.org/idsa/core/>` and target `ids:Resource`. The current IDSA Dataspace Protocol has moved toward DCAT-based self-descriptions:

| ADV uses | Current IDSA/DSP |
|---|---|
| `ids:Resource` | `dcat:Dataset` or `dcat:Resource` |
| `ids:representation` | `dcat:Distribution` |
| `ids:defaultEndpoint` | `dcat:DataService` / `dcat:endpointURL` |
| No policy modelling | `odrl:Policy` for usage control |

The offer template references `ids:representation` and `ids:defaultEndpoint` as placeholders, but these are from the old IDS Information Model (Java-based, pre-DSP).

**Impact:** Offers created with the current templates won't be compatible with production IDSA connectors implementing the Dataspace Protocol.

**Resolution:** Migrate the wrapper to use DCAT vocabulary (`dcat:Dataset`, `dcat:Distribution`, `dcat:DataService`) with `odrl:Policy` for usage constraints, aligned to the DSP catalog protocol.

### 2.4 Property Definitions Not Grounded

In `adv-core.ttl`, properties like `aim:resultTime`, `aim:observedProperty`, `aim:madeBySensor`, etc. are referenced in SHACL shapes but never formally imported or aligned. The core ontology declares:

```turtle
aim:Observation a rdfs:Class .
aim:FeatureOfInterest a rdfs:Class .
```

These are stub declarations — they don't carry any semantics from the actual AIM ontology. This means:
- No RDFS inference can propagate from AIM to ADV
- No OWL reasoner can verify consistency between the two vocabularies
- The declarations serve only as documentation, not as formal alignment

---

## 3. Gap Analysis vs. Industry

### 3.1 What Already Exists

| Standard/Model | What it provides | Overlap with ADV |
|---|---|---|
| **AIM (DEMETER/OGC SWG)** | Agricultural domain semantics: crops, parcels, animals, observations, interventions, alerts | ADV reuses these concepts — no overlap, this is a dependency |
| **Smart Data Models (FIWARE)** | JSON-LD agrifood models with NGSI-LD patterns | Similar entity types (AgriParcel, AgriCrop, etc.) but different governance layer |
| **IDSA Dataspace Protocol** | Data space governance: catalog, negotiation, transfer | ADV should use this for the wrapper layer, not replicate it |
| **INSPIRE** | EU spatial agriculture data (Holdings, Parcels, Sites) | AIM already aligns with INSPIRE; ADV inherits this |
| **DCAT / GeoDCAT-AP** | Dataset metadata and spatial extensions | Should be the vocabulary for ADV's wrapper layer |
| **ODRL** | Usage policy language | Needed for the licence/contract part of ADV offers |

### 3.2 The Unique ADV Contribution (The Gap It Should Fill)

**No existing standard provides the specific binding between agricultural domain content AND data space exchange governance.**

Specifically:
- AIM tells you what agricultural concepts mean
- DCAT/DSP tells you how to describe and discover datasets
- ODRL tells you how to express usage policies
- But **nobody has defined**: "If you want to share soil moisture observations in a data space, here is the minimum set of domain properties the payload must have, here is how the DCAT self-description should reference the profile, and here is how to validate both layers."

**This is the ADV Data Model's unique value proposition:**

> A set of **application profiles** that bind AIM domain semantics to DCAT/DSP data space governance, with SHACL validation for both layers and concrete examples that a pilot developer can use in 10 minutes.

### 3.3 Current Gap Coverage

| Unique contribution | Current status | Gap |
|---|---|---|
| Profile definitions linking AIM to data space exchange | Partially done (5 profiles exist conceptually and as SHACL) | Namespace mismatch prevents real-world use |
| DCAT-based self-descriptions with ADV profile references | Not done — wrapper uses old `ids:Resource` | Need to migrate to DCAT |
| ODRL usage policy patterns for agricultural data | Not done — mentioned in SPARQL.md queries but no shapes/examples | Need policy templates per profile |
| End-to-end validation (wrapper + content + cross-check) | Done in `adv-validate.py` | Works but against wrong namespaces |
| Concrete pilot examples with real data | Not done — examples use synthetic data | Need real pilot data examples |
| Conformance test suite | Partially done — single Python script | Need CI/CD integration, multiple input formats |
| AIM version management | `pinned-import.ttl` exists but points to unresolvable namespace | Need alignment with actual AIM version |

---

## 4. Pilot Readiness Assessment

### 4.1 Can Pilots Use the Current Artefacts?

**Short answer: No, not against real AIM-compliant data.**

The toolbox (D3.2/D3.5) produces data using the DEMETER AIM context (`https://w3id.org/demeter/agri-context.jsonld`), which maps to SOSA/GeoSPARQL/SAREF URIs. An observation from the toolbox looks like:

```json
{
  "@context": "https://w3id.org/demeter/agri-context.jsonld",
  "@type": "sosa:Observation",
  "sosa:resultTime": "2025-09-21T10:35:00Z",
  "sosa:observedProperty": { "@id": "..." },
  "sosa:hasResult": { ... }
}
```

The ADV SHACL shapes target `aim:Observation` and `aim:resultTime` — these will **not match** the toolbox output. The validator would fail on real pilot data.

### 4.2 What's Blocking Pilots

| Blocker | Severity | Effort to fix |
|---|---|---|
| Namespace mismatch (aim: vs sosa:/geo:/etc.) | **Critical** | Medium — requires updating all .ttl and .jsonld files |
| No DCAT wrapper (pilots need IDS connector-compatible self-descriptions) | **High** | Medium — redesign offer templates |
| No ODRL policy examples (pilots need usage conditions) | **Medium** | Low — add policy templates |
| No real pilot data examples | **Medium** | Low-medium — collect from SYN toolbox |
| W3ID namespace not set up (URIs don't resolve) | **Low** (dev phase) | Low — follow w3id/README.md instructions |
| No JSON Schema alternative for non-RDF validators | **Low** | Low — generate from SHACL |

### 4.3 Pilot-Specific Considerations

Based on D3.3 and D3.5:

- **SynField / FieldClimate / Farm21 integrators**: Produce sensor observations (soil moisture, temperature, weather). Need the Observation profile — currently the closest to ready, but namespace fix required.
- **UAV/EO data producers**: Need an EO profile beyond basic Observation. The CHANGELOG mentions "EO product modeling" in v1.0 release notes but no EO-specific profile exists.
- **Livestock pilots (Slovenia, etc.)**: Need Animal profile with richer attributes than current minimum (birthDate, species). Breed, weight, health events are common in practice.
- **CAP compliance use case**: Mentioned in release notes and SPARQL.md but no dedicated profile or SHACL shapes for CAP indicators.

---

## 5. Technical Issues

### 5.1 Validator Path Mismatch

The validator defaults to `--ids-shapes model/ids/ids-wrapper-shapes.ttl` (line 155) but the actual file is at `model/ids-wrapper-shapes.ttl` (no `ids/` subdirectory). The README example uses the correct path, but running the script with defaults would fail.

### 5.2 No JSON-LD Context File for ADV

The ADV model defines terms like `adv:profileId`, `adv:profileVersion`, `adv:externalId`, `adv:issuedAt`, `adv:observedAt` but there is no `adv-context.jsonld` file. Each JSON-LD example manually declares the `adv` prefix in its `@context`. A shared context file would simplify usage and ensure consistency.

### 5.3 JSON-LD @context in Examples Not Production-Ready

The content examples use inline `@context` blocks:
```json
"@context": {
  "aim": "https://w3id.org/aim#",
  "adv": "https://w3id.org/adv/core#",
  ...
}
```

In production, these should reference resolvable URLs (e.g., `"@context": ["https://w3id.org/demeter/agri-context.jsonld", "https://w3id.org/adv/context.jsonld"]`). The current approach works for local testing but not for interoperable exchange.

### 5.4 SHACL Shape Completeness

The shapes are intentionally minimal (good), but some common scenarios are not covered:
- **Observation**: No shape for batch/collection of observations (common in time-series)
- **Parcel-Crop**: No validation of geometry coordinate format
- **Intervention**: Input/output are optional — but a spraying intervention without inputs has limited value
- **Animal**: No group/herd shape (the toolbox has `AnimalGroup`)

### 5.5 No Versioned Release Tags

The CHANGELOG references v1.0.0 and v1.1.0 but the git history shows only two commits with no version tags. Consumers cannot pin to a specific version.

---

## 6. Summary of Findings by Priority

### Critical (Blocks any real-world use)
1. **AIM namespace mismatch** — All `aim:*` references need alignment with actual AIM/DEMETER URIs
2. **IDS wrapper not DSP-compliant** — Must migrate to DCAT vocabulary

### High (Blocks pilot adoption)
3. **No ODRL policy patterns** — Pilots need usage control in their offers
4. **Validator default path incorrect** — Script fails without `--ids-shapes` override
5. **No shared ADV JSON-LD context file** — Increases friction for producers
6. **Legacy D1.3 mappings not formally deprecated** — Creates confusion

### Medium (Reduces value and adoption)
7. **No real pilot data examples** — Synthetic examples don't build confidence
8. **No EO or CAP-specific profiles** — Leaves important use cases uncovered
9. **No JSON Schema alternative** — Excludes non-RDF toolchains
10. **No git version tags** — Consumers can't pin versions

### Low (Polish and industry positioning)
11. **W3ID redirects not configured** — URIs don't resolve
12. **No CI/CD validation pipeline** — Manual validation only
13. **SHACL shapes could be richer** — Batch observations, geometry validation, animal groups
14. **No formal alignment with DSSC vocabularies** — Limits visibility in EU data space ecosystem

---

## 7. Recommendations

The ADV Data Model has a **good architectural design** and a **more complete implementation than most EU project data models at this stage**. The five-profile approach is sound, the SHACL validation is functional, and the developer experience is well thought out.

However, it is currently **disconnected from the real-world implementations it needs to serve** — primarily due to the namespace mismatch with actual AIM and the use of deprecated IDS vocabulary. Fixing these two issues would make the model immediately usable by pilots.

The strategic opportunity is clear: ADV can be the first formalized set of application profiles for agricultural data in data spaces. No one else has done this. But to claim that position, the model must be grounded in the actual standards it references (AIM, DCAT, ODRL) rather than aspirational namespaces.

See **[DEVELOPMENT_PLAN.md](DEVELOPMENT_PLAN.md)** for the phased action plan.
