# ADV Data Model — Migration Guide (v1.x to v2.0)

**Date:** 2026-03-27
**Author:** IDSA / Task 1.3

---

## Summary of Breaking Changes

ADV v2.0 introduces two breaking changes to align the model with real-world implementations:

1. **AIM namespace realignment** — All `aim:*` references replaced with actual upstream URIs (SOSA, GeoSPARQL, SAREF4AGRI, FOODIE).
2. **Wrapper migration from IDS to DCAT** — `ids:Resource` replaced with `dcat:Dataset`; ODRL policies added.

---

## 1. D1.3 Mapping Tables Are Deprecated

The one-to-one class mapping tables from Deliverable D1.3 (Tables 7, 8, 9) are **deprecated**. These mapped concepts like `AgriPest <-> Alert` and `CropType <-> Resource` as class equivalences.

**ADV now uses a profile-driven approach:**
- AIM provides the domain semantics (the "what")
- DCAT/ODRL provides the governance wrapper (the "how")
- ADV profiles bind the two layers with SHACL validation

If you implemented code based on D1.3 mapping tables, migrate to the profile-based approach described in the README.

---

## 2. AIM Namespace Changes

### What changed

All references to `https://w3id.org/aim#` (a namespace that was anticipated but never implemented by the OGC AIM SWG) have been replaced with the actual upstream vocabulary URIs.

### Mapping table

| v1.x (old) | v2.0 (new) | Standard |
|---|---|---|
| `aim:Observation` | `sosa:Observation` | W3C SOSA |
| `aim:FeatureOfInterest` | `sosa:FeatureOfInterest` or `saref4agri:Parcel` | W3C SOSA / SAREF4AGRI |
| `aim:Sensor` | `sosa:Sensor` | W3C SOSA |
| `aim:resultTime` | `sosa:resultTime` | W3C SOSA |
| `aim:observedProperty` | `sosa:observedProperty` | W3C SOSA |
| `aim:madeBySensor` | `sosa:madeBySensor` | W3C SOSA |
| `aim:hasFeatureOfInterest` | `sosa:hasFeatureOfInterest` | W3C SOSA |
| `aim:hasResult` | `sosa:hasResult` | W3C SOSA |
| `aim:value` | `qudt:numericValue` | QUDT |
| `aim:unit` | `qudt:unit` | QUDT |
| `aim:hasGeometry` | `geo:hasGeometry` | OGC GeoSPARQL |
| `aim:hasCrop` | `saref4agri:hasCrop` | ETSI SAREF4AGRI |
| `aim:Crop` | `saref4agri:Crop` | ETSI SAREF4AGRI |
| `aim:cropType` | `foodie:cropSpecies` | FOODIE |
| `aim:area` | `foodie:cropArea` | FOODIE |
| `aim:Activity` | `foodie:Intervention` | FOODIE |
| `aim:activityType` | `dct:type` | Dublin Core |
| `aim:startTime` | `prov:startedAtTime` | W3C PROV |
| `aim:endTime` | `prov:endedAtTime` | W3C PROV |
| `aim:hasInput` | `prov:used` | W3C PROV |
| `aim:hasOutput` | `prov:generated` | W3C PROV |
| `aim:Animal` | `saref4agri:Animal` | ETSI SAREF4AGRI |
| `aim:species` | `schema:species` | Schema.org |
| `aim:birthDate` | `schema:birthDate` | Schema.org |
| `aim:sex` | `schema:gender` | Schema.org |
| `aim:Alert` | `foodie:Alert` | FOODIE |
| `aim:alertType` | `dct:type` | Dublin Core |
| `aim:severity` | `adv:severity` | ADV (no upstream equivalent) |
| `aim:message` | `dct:description` | Dublin Core |

### How to migrate your data

1. **Update `@context`** in your JSON-LD files:
   - Replace `"aim": "https://w3id.org/aim#"` with the individual namespace prefixes (see `model/adv-context.jsonld`).
   - Or use the ADV context directly: `"@context": "https://w3id.org/adv/context.jsonld"`.

2. **Update `@type`** values:
   - `"aim:Observation"` -> `"sosa:Observation"`
   - `"aim:FeatureOfInterest"` -> `"saref4agri:Parcel"` (for parcels) or `"sosa:FeatureOfInterest"` (generic)
   - `"aim:Activity"` -> `"foodie:Intervention"`
   - `"aim:Animal"` -> `"saref4agri:Animal"`
   - `"aim:Alert"` -> `"foodie:Alert"`

3. **Update property names** per the mapping table above.

4. **Re-validate** using the updated validator:
   ```
   python validate/adv-validate.py \
     --wrapper your-offer.jsonld \
     --content your-data.jsonld
   ```

---

## 3. Wrapper Migration (IDS to DCAT)

### What changed

| v1.x (old) | v2.0 (new) |
|---|---|
| `@type: ids:Resource` | `@type: dcat:Dataset` |
| `ids:representation` | `dcat:distribution` |
| `ids:Representation` | `dcat:Distribution` |
| `ids:mediaType` | `dcat:mediaType` |
| `ids:Artifact` | (removed — use `dcat:accessURL` directly) |
| `ids:defaultEndpoint` | `dcat:accessURL` |
| (none) | `dct:conformsTo` (link to ADV profile URI) |
| (none) | `odrl:hasPolicy` (ODRL usage policy) |

### How to migrate your offers

1. **Change `@type`** from `ids:Resource` to `dcat:Dataset`.
2. **Replace the `ids:` prefix** in `@context` with `dcat:` and `odrl:`.
3. **Add `dct:conformsTo`** pointing to the ADV profile URI (e.g., `https://w3id.org/adv/core#observation-v1`).
4. **Add `odrl:hasPolicy`** — use one of the policy templates from `offers/policy-templates/`.
5. **Replace `ids:representation`** with a `dcat:distribution` block containing `dcat:mediaType` and `dcat:accessURL`.

### Wrapper shapes file

- **Old:** `model/ids-wrapper-shapes.ttl`
- **New:** `model/dsp-wrapper-shapes.ttl`

The old file is preserved at `model/ids-wrapper-shapes.ttl` for reference but is no longer used by the validator.

---

## 4. Validator Changes

The validator now:
- Defaults to `model/dsp-wrapper-shapes.ttl` (was `model/ids/ids-wrapper-shapes.ttl`)
- Uses `--wrapper-shapes` flag (the old `--ids-shapes` flag still works but is deprecated)
- Cross-checks against the correct upstream class URIs

---

## 5. New Files in v2.0

| File | Purpose |
|---|---|
| `model/dsp-wrapper-shapes.ttl` | DCAT-based wrapper SHACL (replaces IDS wrapper) |
| `model/odrl-policy-shapes.ttl` | SHACL for ODRL policy validation |
| `model/adv-context.jsonld` | Shared JSON-LD context for all ADV terms |
| `model/adv-aim-profile.ttl` | Documents which upstream terms each profile uses |
| `offers/policy-templates/*.jsonld` | 4 ODRL policy patterns (open, research, attribution, time-limited) |
| `docs/MIGRATION.md` | This file |
