# ADV Data Model — Development Plan

**Date:** 2026-03-27
**Author:** IDSA / Task 1.3
**Version:** Draft for internal alignment

---

## Overview

This plan addresses the findings in [ANALYSIS.md](ANALYSIS.md) and organizes work into three phases:

- **Phase A** — Make the model correct and review-ready (4-6 weeks)
- **Phase B** — Validate with pilots and refine (2-3 months)
- **Phase C** — Position for industry adoption (6-12 months)

Each phase builds on the previous one. Phase A is the minimum viable product for the EU review and real pilot usage.

---

## Phase A — Review-Ready (4-6 weeks)

**Goal:** Fix the critical issues, align with real standards, and produce artefacts that pilots can actually validate data against.

### A.1 Resolve AIM Namespace Alignment (CRITICAL — Week 1-2)

**Problem:** All `aim:*` references point to `https://w3id.org/aim#`, which doesn't exist in the actual AIM OGC SWG repository. Real AIM data uses SOSA, GeoSPARQL, SAREF4AGRI, and DEMETER namespaces.

**Action:**

1. **Determine the correct approach** — Two options:

   - **Option A (Recommended — Direct alignment):** Replace `aim:*` references with the actual upstream URIs. For example:
     - `aim:Observation` → `sosa:Observation` (`http://www.w3.org/ns/sosa/Observation`)
     - `aim:resultTime` → `sosa:resultTime`
     - `aim:madeBySensor` → `sosa:madeBySensor`
     - `aim:hasResult` → `sosa:hasResult`
     - `aim:hasFeatureOfInterest` → `sosa:hasFeatureOfInterest`
     - `aim:FeatureOfInterest` → `sosa:FeatureOfInterest`
     - `aim:hasGeometry` → `geo:hasGeometry` (`http://www.opengis.net/ont/geosparql#hasGeometry`)
     - `aim:Activity` → `https://w3id.org/demeter/agri/agriIntervention#Intervention` or appropriate DEMETER class
     - `aim:Animal` → `saref4agri:Animal` (`https://saref.etsi.org/saref4agri/Animal`)
     - `aim:Alert` → `https://w3id.org/demeter/agri/agriAlert#Alert` or appropriate DEMETER class
     - `aim:hasCrop` → `saref4agri:hasCrop` or `fiware-agrifood:AgriCrop` per AIM alignment
     - `aim:cropType` → appropriate DEMETER/AIM property

   - **Option B (If OGC SWG confirms future namespace):** Keep `aim:*` but create a formal alignment ontology (`model/aim-alignment.ttl`) with `owl:equivalentClass` / `owl:equivalentProperty` triples mapping every `aim:` term to its actual upstream URI. Document the dependency on the future AIM release.

2. **Files to update (Option A):**
   - `model/adv-core.ttl` — Change `aim:` prefix, update class references
   - `model/ids-wrapper-shapes.ttl` — No change needed (doesn't reference AIM)
   - `profiles/observation/shape.ttl` — Replace all `aim:` property paths
   - `profiles/parcel-crop/shape.ttl`
   - `profiles/intervention/shape.ttl`
   - `profiles/animal/shape.ttl`
   - `profiles/alert/shape.ttl`
   - All `content.template.jsonld` files (5) — Update `@context` and property names
   - All `content.sample.jsonld` files (5) — Same
   - `validate/adv-validate.py` — Update `AIM` namespace constant and `PROFILE_TO_AIM` mapping
   - `aim/aim-quick-reference.md` — Rewrite with actual AIM URIs
   - `aim/pinned-import.ttl` — Point to actual AIM ontology URI
   - `docs/translator-alignment.md` — Update property mappings

3. **Create `model/adv-aim-profile.ttl`** — A small ontology that documents which upstream terms each ADV profile uses, providing a single reference point. Example:
   ```turtle
   adv:observation-v1 adv:usesClass sosa:Observation ;
       adv:usesProperty sosa:resultTime, sosa:madeBySensor, sosa:hasResult,
                        sosa:hasFeatureOfInterest, sosa:observedProperty .
   ```

4. **Verify against real AIM context** — Download `https://w3id.org/demeter/agri-context.jsonld` and confirm every term ADV uses is resolvable through it.

**Deliverable:** All ADV artefacts reference real, resolvable URIs from the AIM/DEMETER vocabulary stack.

### A.2 Migrate IDS Wrapper to DCAT/DSP (Week 2-3)

**Problem:** The wrapper uses `ids:Resource` from the deprecated IDS Information Model. Current IDSA Dataspace Protocol uses DCAT.

**Action:**

1. **Redesign `model/ids-wrapper-shapes.ttl`** as `model/dsp-wrapper-shapes.ttl`:
   - Target class: `dcat:Dataset` (instead of `ids:Resource`)
   - Required properties:
     - `dct:title` (string) — unchanged
     - `dct:description` (string) — unchanged
     - `dct:identifier` (string) — unchanged
     - `adv:profileId` — unchanged (ADV-specific)
     - `adv:profileVersion` — unchanged (ADV-specific)
   - Recommended properties:
     - `dct:license` (IRI)
     - `dct:issued` (dateTime)
     - `dct:publisher` (IRI)
     - `dcat:distribution` → `dcat:Distribution` with `dcat:mediaType` and `dcat:accessURL`
   - Optional:
     - `odrl:hasPolicy` → link to an ODRL policy
     - `dcat:temporalResolution`
     - `dcat:spatialResolutionInMeters`
     - `dct:conformsTo` → link to the ADV profile URI

2. **Redesign `offers/offer.template.jsonld` and `offers/offer.sample.jsonld`:**
   - Change `@type` from `ids:Resource` to `dcat:Dataset`
   - Add `dcat:distribution` block
   - Add `odrl:hasPolicy` reference
   - Use `dct:conformsTo` to reference the ADV profile

   Example structure:
   ```json
   {
     "@context": {
       "dcat": "http://www.w3.org/ns/dcat#",
       "dct": "http://purl.org/dc/terms/",
       "odrl": "http://www.w3.org/ns/odrl/2/",
       "adv": "https://w3id.org/adv/core#"
     },
     "@type": "dcat:Dataset",
     "dct:title": "...",
     "dct:description": "...",
     "adv:profileId": "adv.observation",
     "adv:profileVersion": "1.0.0",
     "dct:conformsTo": "https://w3id.org/adv/core#observation-v1",
     "dcat:distribution": {
       "@type": "dcat:Distribution",
       "dcat:mediaType": "application/ld+json",
       "dcat:accessURL": "https://..."
     },
     "odrl:hasPolicy": { ... }
   }
   ```

3. **Update the validator** to target `dcat:Dataset` instead of `ids:Resource`.

4. **Rename the old wrapper shapes** to `model/deprecated/ids-wrapper-shapes-v1.ttl` for historical reference.

**Deliverable:** Wrapper templates and shapes are DSP-compatible and use DCAT vocabulary.

### A.3 Add ODRL Usage Policy Patterns (Week 3)

**Problem:** No usage policy examples. Pilots need to express conditions like "data for research only" or "attribution required."

**Action:**

1. **Create `model/odrl-policy-shapes.ttl`** — Minimal SHACL for validating that an offer includes a policy with at least one permission/prohibition.

2. **Create `offers/policy-templates/`** with 3-4 common patterns:
   - `open-access.jsonld` — CC BY 4.0, no restrictions
   - `research-only.jsonld` — Use limited to research purpose
   - `attribution-required.jsonld` — Must credit the provider
   - `time-limited.jsonld` — Access expires after a period

3. **Update the offer template** to include a default policy reference.

**Deliverable:** Pilots can pick a policy template and include it in their offers.

### A.4 Create ADV JSON-LD Context File (Week 2)

**Problem:** No shared `@context` file for ADV terms. Each example redeclares prefixes manually.

**Action:**

1. **Create `model/adv-context.jsonld`** that maps:
   - All ADV-specific terms (`adv:profileId`, `adv:profileVersion`, `adv:externalId`, `adv:issuedAt`, `adv:observedAt`)
   - References the AIM context (extend, not replace)
   - References DCAT, DCT, ODRL prefixes

2. **Update all JSON-LD files** to reference:
   ```json
   "@context": [
     "https://w3id.org/demeter/agri-context.jsonld",
     "https://w3id.org/adv/context.jsonld"
   ]
   ```

**Deliverable:** Single ADV context file usable by all profiles.

### A.5 Fix Technical Issues (Week 3-4)

1. **Fix validator default path** — Change line 155 from `model/ids/ids-wrapper-shapes.ttl` to `model/dsp-wrapper-shapes.ttl`

2. **Add git version tags** — Tag the current state as `v1.1.0` and the new release as `v2.0.0`

3. **Create `docs/MIGRATION.md`** — Formally deprecate D1.3 mapping tables. Include:
   - What was deprecated and why
   - The new profile-driven approach
   - Mapping from old concepts to new ones

4. **Fix `aim/pinned-import.ttl`** — Point to the actual AIM ontology URI (`https://w3id.org/demeter/agri`)

### A.6 Add End-to-End Examples (Week 4-5)

1. **Create one complete worked example per profile** showing the full chain:
   - Raw data (what comes from the sensor/system)
   - AIM-formatted content payload (JSON-LD)
   - DCAT self-description (the offer)
   - ODRL policy
   - Validation command and expected output

2. **Place in `examples/` directory** (new top-level folder):
   ```
   examples/
     observation-soil-moisture/
       raw-data.csv
       content.jsonld
       offer.jsonld
       policy.jsonld
       README.md  (walk-through)
     parcel-crop-wheat-field/
       ...
   ```

### A.7 Update Documentation (Week 5-6)

1. **Rewrite README.md** — Reflect DCAT migration, correct AIM references
2. **Update CHANGELOG.md** — Document v2.0.0 changes
3. **Create `docs/QUICKSTART.md`** — "Publish your first dataset in 10 minutes" guide
4. **Update `aim/aim-quick-reference.md`** — Use actual AIM/SOSA/GeoSPARQL terms
5. **Update SPARQL.md** — Adjust queries for DCAT-based wrapper

### A.8 Phase A Deliverables Summary

| Artefact | Status after Phase A |
|---|---|
| `model/adv-core.ttl` | Updated with correct AIM references |
| `model/dsp-wrapper-shapes.ttl` | New — replaces ids-wrapper-shapes.ttl |
| `model/odrl-policy-shapes.ttl` | New |
| `model/adv-context.jsonld` | New |
| `model/adv-aim-profile.ttl` | New — documents which upstream terms each profile uses |
| 5x `profiles/*/shape.ttl` | Updated with correct property paths |
| 5x `profiles/*/content.*.jsonld` | Updated with correct @context and properties |
| `offers/offer.*.jsonld` | Migrated to DCAT |
| `offers/policy-templates/*.jsonld` | New — 3-4 ODRL patterns |
| `validate/adv-validate.py` | Updated for DCAT + correct namespaces |
| `examples/` (5 complete worked examples) | New |
| `docs/MIGRATION.md` | New |
| `docs/QUICKSTART.md` | New |
| Updated README, CHANGELOG, quick-reference | Refreshed |

---

## Phase B — Pilot Integration (2-3 months)

**Goal:** Validate the model against real pilot data and refine based on feedback.

### B.1 Collect Real Pilot Data (Month 1)

1. **Work with SYN/Synelixis toolbox team** to:
   - Export sample JSON-LD payloads from the STORE component for each entity type
   - Map toolbox REST API endpoints (`/aim/api/v1/...`) to ADV profiles
   - Run the ADV validator against real toolbox output
   - Document any transformation gaps

2. **Collect data samples from at least 3 pilot sites:**
   - One arable crop pilot (e.g., Greece/SynField — Observation + Parcel-Crop profiles)
   - One livestock pilot (e.g., Slovenia — Animal profile)
   - One advisory/alerting scenario (e.g., pest detection — Alert profile)

3. **Create a `tests/` directory** with real (anonymized) pilot data and expected validation results.

### B.2 Refine Profiles Based on Pilot Feedback (Month 1-2)

Common expected refinements:
- **Observation**: Batch/collection shape for time-series (array of observations)
- **Parcel-Crop**: LPIS parcel identifiers, multi-crop parcels, crop rotation history
- **Intervention**: Nested inputs with active ingredients, equipment references
- **Animal**: Breed, weight, health events, group/herd concept (AnimalGroup)
- **Alert**: Linked advisories (alert → recommended intervention)

### B.3 Platform-Specific Adaptor Guidance (Month 2-3)

Create `docs/adaptors/` with short guides for:
- **SynField** → ADV Observation profile
- **FieldClimate** → ADV Observation profile
- **Farm21** → ADV Observation profile
- **iFarming** → ADV Observation + Parcel-Crop profiles
- **Green Project** → ADV Parcel-Crop + Intervention profiles

Each guide: 1-2 pages showing the platform's data format, the corresponding ADV profile, and the minimal transformation required.

### B.4 Build CI/CD Validation Pipeline (Month 2)

1. **GitHub Actions workflow** that:
   - Validates all sample files against their SHACL shapes on every push
   - Runs the Python validator on all `examples/` worked examples
   - Checks JSON-LD syntax (parseable, no undefined terms)
   - Reports results as PR checks

2. **Docker container** for local validation:
   ```
   docker run ghcr.io/adv-data-model/validator \
     --wrapper offer.jsonld --content data.jsonld
   ```

### B.5 Add JSON Schema Equivalents (Month 3)

For pilots whose toolchains don't support RDF/SHACL:
- Generate JSON Schema from each profile's SHACL shape
- Place alongside the SHACL: `profiles/observation/schema.json`
- Validate with standard JSON Schema validators (ajv, etc.)

### B.6 Phase B Deliverables Summary

| Artefact | Description |
|---|---|
| `tests/` directory | Real pilot data samples + expected validation outcomes |
| Refined SHACL shapes | Accommodating pilot edge cases |
| `docs/adaptors/` | Platform-specific transformation guides |
| GitHub Actions CI | Automated validation on every push |
| Docker validator | Containerized validation tool |
| JSON Schema per profile | Alternative validation for non-RDF toolchains |

---

## Phase C — Industry Positioning (6-12 months)

**Goal:** Make ADV Data Model a recognized standard contribution, not just a project deliverable.

### C.1 OGC Contribution (Month 1-6)

1. **Engage the OGC AIM SWG** — Propose ADV profiles as a set of "AIM Application Profiles for Data Spaces" within the SWG.
2. **Submit an OGC Discussion Paper** or Best Practice document describing the profile pattern.
3. **Ensure ADV profiles are registered** on the OGC Definition Server and AgroPortal.

### C.2 DSSC Alignment (Month 3-6)

1. **Align with Data Spaces Support Centre (DSSC) vocabularies** — Ensure ADV's wrapper (DCAT-based) is compatible with the DSSC blueprint.
2. **Register ADV in the DSSC Building Blocks catalog** as "Agricultural Data Space Application Profiles."
3. **Participate in DSSC semantic interoperability working groups** to position ADV as the reference for agri-food data spaces.

### C.3 Cross-Data-Space Interoperability (Month 6-12)

1. **Test interoperability with other agricultural data spaces:**
   - AGRI-GAIA (German agricultural AI data space)
   - Gaia-X AgriFood
   - Any FIWARE-based agricultural platforms

2. **Create interoperability test events** (plugfests) where multiple implementations validate data exchange using ADV profiles.

### C.4 Standards Publication (Month 9-12)

1. **Publish ADV profiles with persistent identifiers** — Set up w3id.org redirects, ensure all URIs resolve.
2. **Register on AgroPortal** — Make ADV discoverable alongside AIM.
3. **Write a journal/conference paper** positioning ADV as "application profiles bridging agricultural domain models and data space governance."
4. **Create a landing page** at `https://w3id.org/adv/` with documentation, examples, and validator links.

### C.5 Governance Beyond the Project

1. **Define a maintenance model** — Who updates ADV profiles after the project ends? Options:
   - OGC AIM SWG takes ownership
   - IDSA maintains as part of its data space vocabulary portfolio
   - Open community governance (like Schema.org)

2. **Plan for AIM version evolution** — Document how ADV profiles update when AIM releases new versions.

---

## Timeline Summary

```
           Week 1-2   Week 3-4   Week 5-6   Month 2-3  Month 4-6  Month 7-12
           ┌──────────┬──────────┬──────────┬──────────┬──────────┬──────────┐
Phase A    │ A.1 AIM  │ A.2 DCAT │ A.5 Fixes│          │          │          │
           │ namespace│ A.3 ODRL │ A.6 Examp│          │          │          │
           │          │ A.4 Ctx  │ A.7 Docs │          │          │          │
           ├──────────┴──────────┴──────────┤          │          │          │
Phase B    │                                │ B.1-B.6  │          │          │
           │                                │ Pilot    │          │          │
           │                                │ validate │          │          │
           ├────────────────────────────────┴──────────┤          │          │
Phase C    │                                           │ C.1-C.2  │ C.3-C.5  │
           │                                           │ OGC/DSSC │ Standards│
           └───────────────────────────────────────────┴──────────┴──────────┘
```

---

## Decision Points

Before starting implementation, the following decisions need stakeholder alignment:

### Decision 1: AIM Namespace Strategy
- **Option A**: Align directly with SOSA/GeoSPARQL/DEMETER URIs (recommended — works today)
- **Option B**: Keep `aim:` namespace with alignment ontology (depends on OGC SWG confirming the namespace migration)

**Who decides:** IDSA (lead) + OGC AIM SWG liaison
**Deadline:** Before Phase A implementation starts

### Decision 2: Version Number
- Phase A changes are breaking (namespace + wrapper redesign) → suggests **v2.0.0**
- Alternative: call it v1.2.0 if the `aim:` namespace is treated as a placeholder that was always meant to be replaced

**Who decides:** IDSA
**Deadline:** Before Phase A.7 (documentation update)

### Decision 3: Scope of Phase B Pilot Engagement
- Minimum: 3 pilots (one per major type: arable, livestock, advisory)
- Recommended: 5+ pilots covering all profiles
- Maximum: All 11 pilot sites

**Who decides:** IDSA + WP3 lead (SYN)
**Deadline:** End of Phase A

### Decision 4: OGC Submission Vehicle
- Discussion Paper (lower bar, faster)
- Best Practice document (higher recognition)
- Standard (ambitious, longer timeline)

**Who decides:** IDSA + OGC AIM SWG
**Deadline:** Phase C planning (Month 4)

---

## Resource Requirements

| Phase | Effort | Key dependencies |
|---|---|---|
| Phase A | ~120-160 person-hours (ontology engineer + developer) | Access to AIM OGC SWG repository; confirmation of namespace strategy |
| Phase B | ~200-300 person-hours (ontology engineer + pilot integrators) | Cooperation from SYN toolbox team; pilot site availability |
| Phase C | ~100-200 person-hours (standards expert + ontology engineer) | OGC SWG engagement; DSSC contact |

---

## Risk Register

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| AIM namespace change breaks ADV again | Medium | High | Use upstream URIs (SOSA/GeoSPARQL) directly; wrap in ADV context |
| Pilots don't engage in Phase B | Medium | High | Start with SYN toolbox (already using AIM); provide ready-made adaptors |
| IDSA DSP specification changes | Low | Medium | Use DCAT core (stable W3C standard) as anchor; DSP-specific parts are thin |
| OGC SWG doesn't accept contribution | Medium | Low | Publish independently at w3id.org; OGC submission is additive, not required |
| Project review finds artefacts insufficient | Low after Phase A | High | Phase A specifically targets review readiness |

---

## Success Criteria

### Phase A (Review-Ready)
- [ ] All SHACL shapes validate against real AIM-formatted data
- [ ] Wrapper shapes are DCAT-compatible
- [ ] Validator runs successfully on all example files
- [ ] At least one worked example per profile with real-world data patterns
- [ ] README enables a developer to publish their first ADV-compliant dataset in under 30 minutes

### Phase B (Pilot-Validated)
- [ ] At least 3 pilot sites have successfully validated their data against ADV profiles
- [ ] Each profile has been tested with at least 2 different data sources
- [ ] CI/CD pipeline passes on every commit
- [ ] JSON Schema alternative available for all 5 profiles

### Phase C (Industry-Recognized)
- [ ] ADV profiles registered on AgroPortal
- [ ] At least one OGC submission (Discussion Paper or better)
- [ ] W3ID URIs resolve to documentation
- [ ] At least one cross-data-space interoperability test completed
- [ ] Post-project maintenance model agreed
