# Data Transformation Guides

This folder contains guides for transforming data from common source formats into ADV-compliant JSON-LD.

## Available Guides

| Source format | Guide | Target profiles |
|--------------|-------|-----------------|
| Flat CSV | [csv-to-adv.md](csv-to-adv.md) | All 5 profiles |
| NGSI-LD / FIWARE | [ngsi-ld-to-adv.md](ngsi-ld-to-adv.md) | Observation, Parcel-Crop, Animal |

## General Approach

All transformations follow the same pattern:

1. **Map your source fields** to ADV profile column names (see `profiles/*/csv-template.csv`).
2. **Run the ADV transformer** to produce JSON-LD:
   ```bash
   python validate/adv-transform.py --profile observation --input my-data.csv --output my-data.jsonld
   ```
3. **Validate** the output:
   ```bash
   python validate/adv-validate.py --content my-data.jsonld --content-only --profile observation
   ```

If your source format is not CSV, convert it to the ADV CSV template format first, then use the transformer. Alternatively, produce JSON-LD directly following the templates in `profiles/*/content.template.jsonld`.
