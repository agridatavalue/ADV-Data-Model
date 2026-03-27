# ADV Data Model — Quickstart Guide

Get from zero to a validated ADV-compliant dataset in 15 minutes.

**Prerequisites:** Python 3.10+ installed.

---

## Step 1 — Clone and Set Up (2 min)

```bash
git clone https://github.com/your-org/ADV-IDSA-DATA_MODEL.git
cd ADV-IDSA-DATA_MODEL
pip install -r validate/requirements.txt
```

## Step 2 — Choose Your Profile (1 min)

Pick the profile that matches your data:

| Your data | Profile | Template |
|-----------|---------|----------|
| Sensor readings (temperature, moisture, etc.) | **observation** | `profiles/observation/content.template.jsonld` |
| Field boundaries and crops | **parcel-crop** | `profiles/parcel-crop/content.template.jsonld` |
| Spraying, irrigation, fertilisation records | **intervention** | `profiles/intervention/content.template.jsonld` |
| Animal identification and records | **animal** | `profiles/animal/content.template.jsonld` |
| Pest, disease, or weather alerts | **alert** | `profiles/alert/content.template.jsonld` |

## Step 3 — Create Your Content File (5 min)

Copy the template and replace the placeholder values:

```bash
cp profiles/observation/content.template.jsonld my-data.jsonld
```

Open `my-data.jsonld` in any text editor. Replace every `REPLACE_*` value. For example:

```json
{
  "@type": "sosa:Observation",
  "sosa:resultTime": { "@value": "2025-09-21T10:35:00Z", "@type": "xsd:dateTime" },
  "sosa:observedProperty": { "@id": "https://w3id.org/phenomenon/soilMoisture" },
  ...
}
```

**Key rules:**
- Values marked as IRI in the template must use `{"@id": "https://..."}` syntax
- Date/time values must use `{"@value": "...", "@type": "xsd:dateTime"}` syntax
- String values (like `adv:externalId`) are plain strings: `"my-id-123"`

See `docs/VOCABULARY_GUIDE.md` for where to find IRIs for crop types, species, units, etc.

## Step 4 — Create Your Offer File (3 min)

Copy the offer template:

```bash
cp offers/offer.template.jsonld my-offer.jsonld
```

Fill in:
- `dct:title` — A human-readable name for your dataset
- `dct:description` — What, where, when
- `dct:identifier` — A stable ID
- `adv:profileId` — One of: `adv.observation`, `adv.parcel-crop`, `adv.intervention`, `adv.animal`, `adv.alert`
- `dcat:accessURL` — Where the data can be accessed (use `{"@id": "https://..."}` syntax)

Choose a policy from `offers/policy-templates/` and reference it, or embed one directly.

## Step 5 — Validate (2 min)

```bash
python validate/adv-validate.py \
  --wrapper my-offer.jsonld \
  --content my-data.jsonld
```

If everything passes:
```
All checks passed.
```

If something fails, the error messages tell you exactly which property is missing or malformed.

## Step 6 — Publish

Your validated data package (content + offer + policy) is ADV-compliant and ready to be shared through an IDSA connector or any DCAT-compatible catalog.

---

## Quick Reference

| What | Where |
|------|-------|
| SHACL shapes | `profiles/<profile>/shape.ttl` |
| JSON-LD context file | `model/adv-context.jsonld` |
| DCAT wrapper shapes | `model/dsp-wrapper-shapes.ttl` |
| Policy templates | `offers/policy-templates/` |
| Full worked example | `examples/observation-soil-moisture/` |
| AIM vocabulary cheat sheet | `aim/aim-quick-reference.md` |
| IRI vocabulary sources | `docs/VOCABULARY_GUIDE.md` |

---

## Common Mistakes

1. **Forgetting `{"@id": "..."}` for IRI values.** Writing `"sosa:observedProperty": "https://..."` produces a string literal. It must be `"sosa:observedProperty": {"@id": "https://..."}`.

2. **Forgetting `{"@value": "...", "@type": "xsd:dateTime"}` for dates.** Writing `"sosa:resultTime": "2025-09-21T10:35:00Z"` produces an untyped string. The SHACL shape requires `xsd:dateTime`.

3. **Using the wrong profileId.** The `adv:profileId` in the offer must match the `@type` in the content. The validator cross-checks this.

4. **Giving nested references a `@type`.** If you reference another entity (e.g., a parent animal), use only `{"@id": "..."}` — don't add `@type` unless you also provide all required properties for that type.
