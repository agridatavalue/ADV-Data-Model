# D3 Plan

## 1. Purpose

D3 must take the ADV Data Model from its current "structurally complete but not yet field-tested" state to a level where:

- **Pilot integrators** can validate real data against the profiles without assistance.
- **Third parties** outside the consortium can understand, evaluate, and reuse the model within 30 minutes of opening the repository.
- **Reviewers** (EU, OGC, DSSC) can verify that the model does what it claims — bind agricultural domain semantics to data space governance — with traceable evidence from artefact to artefact.

The repository already contains the right architecture (profile-driven, two-layer, SHACL-validated). The work remaining is to make it verifiably correct, internally consistent, and practically usable by people who did not build it.

---

## 2. Current State of the Repository

### 2.1 Structure

The repo contains approximately 47 files organised into a clear folder layout:

| Folder | Contents |
|--------|----------|
| `model/` | Core ontology (`adv-core.ttl`), DCAT wrapper shapes, ODRL policy shapes, JSON-LD context, AIM profile manifest, plus deprecated IDS wrapper shapes |
| `profiles/` | 5 subdirectories (observation, parcel-crop, intervention, animal, alert), each with SHACL shape, JSON-LD template, JSON-LD sample, CSV template |
| `offers/` | DCAT offer template + sample, plus 4 ODRL policy templates |
| `aim/` | AIM quick reference and pinned import stub |
| `validate/` | Python validator script |
| `registry/` | FAIR metadata registry (JSON) |
| `docs/` | Analysis, development plan, migration guide, SPARQL queries, translator alignment, v1.0 release notes |
| `w3id/` | Namespace redirect setup instructions |

### 2.2 Version and Recent Changes

The repo is at version **2.0.0** (dated 2026-03-27). This version performed a full namespace realignment (replacing a placeholder `aim:` namespace with real upstream URIs from SOSA, GeoSPARQL, SAREF4AGRI, FOODIE) and migrated the wrapper layer from the deprecated IDS Information Model to DCAT/ODRL. These changes touched all SHACL shapes, all JSON-LD files, the validator, the offer templates, and the documentation.

### 2.3 Usability Assessment

The repo is navigable. A technically literate person can find the main artefacts within a few minutes. The README provides a 5-step usage flow. The SHACL shapes are well-commented. The JSON-LD samples are readable. However, several consistency and completeness gaps remain that would hinder a third party attempting unassisted adoption — detailed in Section 4.

---

## 3. Key Strengths

1. **Clean two-layer architecture.** The separation between domain content (profile SHACL targeting upstream vocabulary classes) and governance wrapper (DCAT/ODRL SHACL targeting `dcat:Dataset`) is implemented, not just described. Both layers have independent SHACL shapes and the validator cross-checks them.

2. **Real upstream URIs.** The v2.0 namespace migration means that SHACL shapes target actual W3C, OGC, and ETSI classes (`sosa:Observation`, `geo:hasGeometry`, `saref4agri:Parcel`, `foodie:Intervention`, etc.). This is the single most important quality — it means ADV data can coexist with other AIM-compliant data without URI conflicts.

3. **Consistent profile pattern.** Every profile follows the same structure: `shape.ttl` + `content.template.jsonld` + `content.sample.jsonld` + `csv-template.csv`. This makes the model predictable and extensible.

4. **Working validator.** The Python script performs wrapper validation, content validation, and wrapper-content cross-checking in one command. It auto-detects the profile from the wrapper's `adv:profileId`.

5. **ODRL policy templates.** Four reusable policy patterns (open access, research-only, attribution-required, time-limited) are immediately usable. This is a practical differentiator — most data models stop before usage control.

6. **Shared JSON-LD context file.** `model/adv-context.jsonld` maps short names to full upstream URIs, enabling JSON-LD producers to use readable property names without manually declaring prefixes.

7. **Explicit migration path.** `docs/MIGRATION.md` provides a complete old-to-new mapping table for the v1.x → v2.0 transition, including wrapper, content, and validator changes.

---

## 4. Key Gaps and Risks

### 4.1 Validation Has Not Been Verified

The v2.0 changes touched every SHACL shape and every JSON-LD file simultaneously. **There is no evidence in the repository that the validator has been run against the updated sample files.** The sample files may not pass the updated SHACL shapes due to subtle serialisation mismatches (e.g., datatype handling in JSON-LD, blank node expansion). Until this is confirmed, the artefacts are structurally plausible but not verified.

**Risk: HIGH.** A third party running the validator on the provided samples and getting failures would undermine confidence in the entire model.

### 4.2 CSV Templates Not Updated

The five CSV templates still use column header names from v1.x (e.g., `activityTypeIRI` in the intervention CSV). While these are human-readable labels and not formal URIs, they are inconsistent with the new property names used in the SHACL shapes and JSON-LD files. No CSV-to-JSON-LD conversion guidance exists.

### 4.3 FAIR Registry Is Stale

`registry/artifacts-metadata-json` references v1.0.0 artefacts and an incorrect path (`model/ids/ids-wrapper-shapes.ttl`). It does not list any v2.0 files (DCAT wrapper shapes, ODRL shapes, context file, profile manifest, policy templates). The README references `registry/artifacts-metadata.json` (with `.json` extension) but the actual file has no extension.

### 4.4 Deprecated Artefacts Not Clearly Isolated

`model/ids-wrapper-shapes.ttl` (deprecated) sits alongside `model/dsp-wrapper-shapes.ttl` (current) with no directory-level separation. An empty file `model/ids` also exists as debris. A newcomer could mistake the deprecated file for the active one.

### 4.5 Example IRIs Are Not Resolvable

Sample files use IRIs like `https://w3id.org/phenomenon/soilMoisture`, `https://w3id.org/crop/Wheat`, `https://w3id.org/species/Bos_taurus`, `https://w3id.org/alertType/Pest`, and `https://w3id.org/severity/High`. None of these resolve. There is no controlled vocabulary or code list backing them. A pilot implementer filling in the templates would have no guidance on what IRIs to use for their own data.

### 4.6 `schema:species` Does Not Exist in Schema.org

The Animal profile uses `schema:species` as a required property. Schema.org does not define a property called `species`. This means the expanded URI `https://schema.org/species` has no formal definition. This is a semantic accuracy problem that should be resolved before external review.

### 4.7 JSON-LD Samples Do Not Reference the Shared Context

Each JSON-LD sample file declares its own inline `@context` block. None of them reference `model/adv-context.jsonld`. This makes the context file orphaned — it exists but is not demonstrated in use. Producers following the samples will not learn about or use the shared context.

### 4.8 No End-to-End Worked Example

There is no single directory that shows the complete chain: raw input → content payload → DCAT offer → ODRL policy → validation command → expected output. The README describes the steps, but no concrete artefact demonstrates them together.

### 4.9 No CI/CD or Automated Validation

Validation is manual. There is no GitHub Actions workflow, no `requirements.txt` for Python dependencies, and no documented way to run all validations at once.

### 4.10 Internal Analysis Documents Mixed with User-Facing Docs

`docs/ANALYSIS.md` and `docs/DEVELOPMENT_PLAN.md` are internal assessment documents that describe what was wrong with v1.x. They are valuable for the team but confusing for an external visitor who might interpret them as describing the current state. `docs/RELEASE_NOTES_v1.0.md` references a repository structure (`model/adv.ttl`, `model/shapes.ttl`) that no longer exists.

### 4.11 No Architecture Diagram

The two-layer model (domain content + governance wrapper) is the defining feature of ADV, but it is only described in prose. A visual diagram would make it immediately clear to any reader.

---

## 5. D3 Objectives

1. **Verify correctness.** Confirm that every sample file passes validation against every corresponding SHACL shape, and that the cross-check logic works.
2. **Achieve full internal consistency.** Ensure that all artefacts (SHACL, JSON-LD, CSV, context file, registry, documentation) reflect the same v2.0 vocabulary decisions without contradiction.
3. **Enable unassisted third-party adoption.** A developer or data engineer outside the consortium should be able to produce a valid ADV-compliant dataset using only what is in this repository.
4. **Prepare for external review.** Make the repository presentable to EU reviewers, OGC SWG members, and DSSC representatives without requiring oral explanation.

---

## 6. Scope of Work

### In Scope
- Validation testing and bug fixing across all artefacts
- Consistency fixes (CSV templates, registry, deprecated file cleanup)
- Semantic accuracy fixes (e.g., `schema:species`)
- One complete end-to-end worked example
- A quickstart guide and architecture diagram
- CI/CD pipeline for automated validation
- IRI guidance (recommended code lists / vocabulary sources for property values)
- Documentation restructuring for external readability

### Out of Scope
- Adding new profiles (EO, CAP, market data) — this is Phase B/C work
- Collecting real pilot data — depends on external partners
- W3ID registration — depends on external PR to perma-id/w3id.org
- OGC or DSSC submission — depends on Phase C decisions
- JSON Schema generation — lower priority, deferrable

---

## 7. Workstreams

### WS-1: Verification and Correctness

Run the validator against every sample/offer pair. Fix any SHACL-vs-JSON-LD mismatches. Ensure the cross-check logic correctly maps `adv:profileId` to the upstream class. Resolve the `schema:species` issue (replace with a term that actually exists in the referenced vocabulary, or define it explicitly in `adv-core.ttl` with a rationale comment).

### WS-2: Consistency and Cleanup

Update CSV templates to align column names with v2.0 properties. Update the FAIR registry with all v2.0 artefacts and correct paths. Move deprecated files to a `model/deprecated/` directory. Remove the empty `model/ids` file. Ensure JSON-LD samples demonstrate the shared context file (at least one sample per profile should show usage of `model/adv-context.jsonld` alongside the inline variant).

### WS-3: Onboarding and Third-Party Usability

Create one complete end-to-end worked example (recommended: Observation profile, soil moisture scenario) in an `examples/` directory. Create `docs/QUICKSTART.md` — a self-contained guide that gets a new user from zero to a validated dataset in under 15 minutes. Add an architecture diagram (ASCII or SVG) to the README showing the two-layer model. Restructure `docs/` to separate internal planning documents from user-facing guides. Add a `requirements.txt` for the validator.

### WS-4: IRI Guidance and Vocabulary Signposting

Create `docs/VOCABULARY_GUIDE.md` documenting recommended vocabulary sources for IRI-typed fields: where to find crop type IRIs (AGROVOC, EPPO), species IRIs (NCBI Taxonomy, Wikidata), unit IRIs (QUDT unit vocabulary), observation property IRIs (observable property registries). This does not require ADV to host controlled vocabularies — it requires signposting existing ones.

### WS-5: CI/CD and Automated Quality

Create a GitHub Actions workflow that runs the validator against all 5 sample files on every push. Add a simple `Makefile` or script (`validate/run-all.sh`) that validates all profiles in one command. Add `requirements.txt` listing `rdflib` and `pyshacl` with pinned versions.

---

## 8. Planned Artefacts and Outputs

| # | Artefact | Action | Workstream |
|---|----------|--------|------------|
| 1 | All 5 `content.sample.jsonld` + `offer.sample.jsonld` | Verify pass validation; fix if needed | WS-1 |
| 2 | `profiles/animal/shape.ttl` — `schema:species` | Replace with valid upstream term or define in `adv-core.ttl` | WS-1 |
| 3 | 5 CSV templates | Update column headers to match v2.0 property names | WS-2 |
| 4 | `registry/artifacts-metadata.json` | Rewrite for v2.0; add all new files; fix file extension | WS-2 |
| 5 | `model/deprecated/` directory | Move `ids-wrapper-shapes.ttl` there; remove `model/ids` | WS-2 |
| 6 | JSON-LD samples | Add one variant per profile using `adv-context.jsonld` as `@context` | WS-2 |
| 7 | `examples/observation-soil-moisture/` | Full chain: content + offer + policy + validation command + expected output | WS-3 |
| 8 | `docs/QUICKSTART.md` | 15-minute guide from clone to validated dataset | WS-3 |
| 9 | Architecture diagram in README | ASCII or inline SVG showing two-layer model | WS-3 |
| 10 | `docs/internal/` directory | Move `ANALYSIS.md`, `DEVELOPMENT_PLAN.md`, `RELEASE_NOTES_v1.0.md` there | WS-3 |
| 11 | `validate/requirements.txt` | Pin `rdflib` and `pyshacl` versions | WS-3 |
| 12 | `docs/VOCABULARY_GUIDE.md` | Recommended IRI sources for crop types, species, units, observed properties | WS-4 |
| 13 | `.github/workflows/validate.yml` | GitHub Actions CI for all profiles | WS-5 |
| 14 | `validate/run-all.sh` | Batch validation script | WS-5 |

---

## 9. Phased Implementation Plan

### Phase 1 — Verify and Fix (Priority: Critical, ~1 week)

**Goal:** Confirm the artefacts actually work.

1. Install validator dependencies (`pip install rdflib pyshacl`).
2. Run `adv-validate.py` against all 5 profile samples with `offer.sample.jsonld` as wrapper.
3. Document every failure. Fix SHACL or JSON-LD as needed.
4. Resolve the `schema:species` issue in the Animal profile.
5. Run validation again. All 5 must pass cleanly.

**Dependency:** Nothing else should proceed until this is green.

### Phase 2 — Consistency Pass (Priority: High, ~1 week)

**Goal:** Every artefact reflects v2.0 consistently.

1. Update CSV templates.
2. Rewrite the FAIR registry.
3. Move deprecated files to `model/deprecated/`.
4. Add shared context demonstration to at least one JSON-LD sample per profile.
5. Verify that `adv-context.jsonld` correctly expands all terms used in the samples.

### Phase 3 — Onboarding and Documentation (Priority: High, ~2 weeks)

**Goal:** A third party can adopt the model without help.

1. Create the end-to-end worked example.
2. Write `docs/QUICKSTART.md`.
3. Add the architecture diagram to the README.
4. Restructure `docs/` (move internal files to `docs/internal/`).
5. Create `validate/requirements.txt`.
6. Write `docs/VOCABULARY_GUIDE.md`.

### Phase 4 — Automation (Priority: Medium, ~1 week)

**Goal:** Quality stays verified over time.

1. Create `validate/run-all.sh`.
2. Create `.github/workflows/validate.yml`.
3. Confirm CI passes on the current state.

---

## 10. Roles and Responsibilities

| Role | Responsibilities |
|------|-----------------|
| **Semantic lead** (ontology/vocabulary expertise) | WS-1 (validation, `schema:species` fix, SHACL correctness), WS-2 (context file alignment), WS-4 (vocabulary guide) |
| **Developer / tooling lead** | WS-1 (running validator, debugging), WS-5 (CI/CD, batch script, requirements.txt) |
| **Documentation lead** | WS-3 (quickstart, worked example, architecture diagram, docs restructure) |
| **All contributors** | Review Phase 1 results before proceeding to Phase 2 |

In practice, the semantic lead and documentation lead may be the same person given the team size. The critical constraint is that the person running WS-1 must understand both SHACL validation mechanics and JSON-LD serialisation rules.

---

## 11. Validation and Quality Control

### Automated Checks (per push, once CI is in place)
- All 5 profile samples pass SHACL validation against their corresponding shape.
- The offer sample passes DCAT wrapper shape validation.
- Cross-check (wrapper `profileId` vs content `@type`) passes for all 5 pairs.
- JSON-LD files parse without errors (`rdflib` can load them).

### Manual Review Gates
- **After Phase 1:** Review all validation outputs. Confirm 5/5 clean passes. Sign off before proceeding.
- **After Phase 2:** Spot-check that CSV headers, registry entries, and context file term mappings are consistent with each SHACL shape.
- **After Phase 3:** Have someone who has never seen the repo before attempt to follow the quickstart guide. Note where they get stuck. Fix those points.
- **After Phase 4:** Verify CI runs green on a clean clone.

### Semantic Review
- Verify that every `sh:targetClass` in every SHACL shape references a URI that is formally defined in the vocabulary it claims (SOSA, GeoSPARQL, SAREF4AGRI, FOODIE).
- Verify that every `sh:path` property in every SHACL shape references a URI that is formally defined in the vocabulary it claims.
- Document any ADV-minted terms (`adv:severity`, `adv:productionType`, `adv:hasParent`) and confirm they are declared in `adv-core.ttl`.

---

## 12. Third-Party Usability Requirements

For a third party to successfully use this repository, the following must be true:

1. **The README explains what ADV is, who it is for, and what it does — in the first 10 lines.** Currently adequate.

2. **A quickstart guide exists that does not require prior knowledge of SHACL, JSON-LD, or DCAT.** Currently missing. The README's 5-step guide assumes the reader understands JSON-LD structure and SHACL validation concepts.

3. **Every sample file included in the repo passes the included validator.** Not yet verified.

4. **The validator can be installed and run with a single documented command.** Requires `requirements.txt` and documented `pip install` + run instructions.

5. **At least one complete end-to-end example exists** showing raw data → ADV content → DCAT offer → policy → validation. Currently missing.

6. **IRI-typed fields have guidance on what IRIs to use.** Currently missing. A producer encountering `sosa:observedProperty` as a required IRI field has no guidance on which vocabulary to draw from.

7. **The architecture (two-layer model) is visually explained.** Currently prose only.

8. **Deprecated artefacts are clearly separated from current ones.** Currently `ids-wrapper-shapes.ttl` sits alongside active files with no marker.

9. **Internal planning documents are not mixed with user-facing docs.** Currently `ANALYSIS.md` and `DEVELOPMENT_PLAN.md` (internal) sit in the same folder as `MIGRATION.md` and `SPARQL.md` (user-facing).

10. **The repository has automated validation** so that third-party contributors can verify their changes pass. Currently manual only.

---

## 13. Immediate Next Actions

1. **Run the validator now** against all 5 profile samples and the offer sample. Record the results. This is the single highest-priority action.

   ```
   python validate/adv-validate.py --wrapper offers/offer.sample.jsonld --content profiles/observation/content.sample.jsonld
   python validate/adv-validate.py --wrapper offers/offer.sample.jsonld --content profiles/parcel-crop/content.sample.jsonld
   python validate/adv-validate.py --wrapper offers/offer.sample.jsonld --content profiles/intervention/content.sample.jsonld
   python validate/adv-validate.py --wrapper offers/offer.sample.jsonld --content profiles/animal/content.sample.jsonld
   python validate/adv-validate.py --wrapper offers/offer.sample.jsonld --content profiles/alert/content.sample.jsonld
   ```

2. **Fix any validation failures** before doing anything else.

3. **Investigate `schema:species`** — confirm whether Schema.org defines it. If not, choose an alternative (e.g., define `adv:species` explicitly, or use a SAREF4AGRI / SmartDataModels term with evidence).

4. **Create `validate/requirements.txt`** with `rdflib` and `pyshacl`.

5. **Move `model/ids-wrapper-shapes.ttl` to `model/deprecated/`** and delete the empty `model/ids` file.

6. **Assign Phase 1 owner** and set a one-week deadline.
