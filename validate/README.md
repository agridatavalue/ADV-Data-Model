# ADV Validator

Validates ADV data packages against SHACL shapes. Checks both the DCAT governance wrapper and the domain content, and cross-checks that they reference the same profile.

## Installation

```bash
pip install -r validate/requirements.txt
```

Requires Python 3.10+.

## Usage

### Full validation (wrapper + content)

The standard mode. Validates the offer wrapper, the content payload, and cross-checks that `adv:profileId` matches the content `@type`.

```bash
python validate/adv-validate.py \
  --wrapper offers/offer.sample.jsonld \
  --content profiles/observation/content.sample.jsonld
```

The profile SHACL shape is auto-detected from the wrapper's `adv:profileId`.

### Content-only validation

Validate just your content file during development — no offer wrapper needed.

```bash
python validate/adv-validate.py \
  --content my-data.jsonld \
  --content-only --profile observation
```

Available profile names: `observation`, `parcel-crop`, `intervention`, `animal`, `alert`.

### Override shapes paths

```bash
python validate/adv-validate.py \
  --wrapper my-offer.jsonld \
  --content my-data.jsonld \
  --wrapper-shapes model/dsp-wrapper-shapes.ttl \
  --profile-shapes profiles/observation/shape.ttl
```

### Batch validation (all profiles)

```bash
bash validate/run-all.sh
```

Validates all 5 profile samples with auto-generated wrappers. Used by CI.

## Flags

| Flag | Required | Default | Description |
|------|----------|---------|-------------|
| `--wrapper` | Yes (unless `--content-only`) | — | Path to DCAT wrapper JSON-LD |
| `--content` | Yes | — | Path to domain content JSON-LD |
| `--content-only` | No | off | Skip wrapper validation; validate content only |
| `--profile` | Only with `--content-only` | — | Profile name (observation, parcel-crop, etc.) |
| `--wrapper-shapes` | No | `model/dsp-wrapper-shapes.ttl` | Custom wrapper SHACL path |
| `--profile-shapes` | No | Auto-detected | Custom profile SHACL path |
| `--ids-shapes` | No | — | Deprecated alias for `--wrapper-shapes` |

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | All checks passed |
| 1 | Wrapper failed, content passed |
| 2 | Content failed, wrapper passed (or content-only mode failed) |
| 3 | Both wrapper and content failed |
| 4 | Usage error, missing file, or runtime error |

## What Gets Checked

1. **Wrapper SHACL** — The offer file must be a valid `dcat:Dataset` with required fields (`dct:title`, `dct:description`, `dct:identifier`, `adv:profileId`, `adv:profileVersion`).

2. **Content SHACL** — The content file must conform to the profile's shape (e.g., `sosa:Observation` must have `sosa:resultTime`, `sosa:observedProperty`, etc.).

3. **Cross-check** — The `adv:profileId` in the wrapper (e.g., `adv.observation`) must match the `@type` in the content (e.g., `sosa:Observation`).

## Common Errors and Fixes

**"Value node is a Literal, expected IRI"**
Your JSON-LD has `"sosa:observedProperty": "https://..."` — a plain string. Use `{"@id": "https://..."}` instead.

**"Datatype mismatch for xsd:dateTime"**
Your date is a plain string. Use `{"@value": "2025-09-21T10:35:00Z", "@type": "xsd:dateTime"}`.

**"Wrapper/content mismatch"**
The `adv:profileId` in your offer doesn't match what's in the content. Check that you're using the right profile.

**"Could not find adv:profileId in wrapper"**
Your offer file is missing `adv:profileId`. Add it (e.g., `"adv:profileId": "adv.observation"`).
