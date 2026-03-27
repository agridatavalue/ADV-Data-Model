# CSV to ADV JSON-LD

The ADV repository includes a transformer script that converts CSV files into validated JSON-LD. This is the fastest path to producing ADV-compliant data.

## Prerequisites

```bash
pip install -r validate/requirements.txt
```

## Step 1 — Prepare Your CSV

Each profile has a CSV template in `profiles/<profile>/csv-template.csv`. Your CSV must use the same column headers.

### Observation Profile

```csv
externalId,resultTime,observedProperty,madeBySensor,featureOfInterest,value,unit,issuedAt
MY-SENSOR-001,2025-09-21T10:35:00Z,https://w3id.org/phenomenon/soilMoisture,https://data.my-org.org/sensor/S1,https://data.my-org.org/parcel/P1,0.23,http://qudt.org/vocab/unit/VolumeFraction,2025-09-21T10:35:02Z
```

### Parcel-Crop Profile

```csv
externalId,geometryType,geometryCoordinatesWGS84,cropInstanceId,cropSpeciesIRI,cropArea,issuedAt
Field-A,Polygon,"[[[3.74,51.01],[3.75,51.01],[3.75,51.00],[3.74,51.00],[3.74,51.01]]]",crop-2025,https://w3id.org/crop/Wheat,2.45,2025-03-15T12:00:00Z
```

**Note:** The geometry coordinates column must contain valid JSON (a nested array of coordinate pairs).

### Intervention Profile

```csv
externalId,typeIRI,startedAtTime,endedAtTime,featureOfInterest,usedId,usedQuantity,usedUnitIRI,generatedId,generatedQuantity,generatedUnitIRI,issuedAt
OPS-001,https://w3id.org/activity/Spraying,2025-04-10T06:30:00Z,2025-04-10T07:45:00Z,https://data.my-org.org/parcel/P1,https://data.my-org.org/material/M1,120.0,http://qudt.org/vocab/unit/Liter,,,,2025-04-10T08:00:00Z
```

**Note:** Leave `usedId`/`generatedId` columns empty if no input or output applies.

### Animal Profile

```csv
externalId,speciesIRI,birthDate,sexIRI,productionTypeIRI,parentId,issuedAt
COW-1245,https://w3id.org/species/Bos_taurus,2021-03-14,https://w3id.org/vocab/sex/Female,https://w3id.org/vocab/productionType/Dairy,,2025-01-05T09:30:00Z
```

### Alert Profile

```csv
externalId,typeIRI,severityIRI,description,featureOfInterest,startedAtTime,endedAtTime,issuedAt
ALERT-001,https://w3id.org/alertType/Pest,https://w3id.org/severity/High,"Aphid risk in Field A",https://data.my-org.org/parcel/P1,2025-06-02T08:00:00Z,2025-06-05T18:00:00Z,2025-06-02T07:55:00Z
```

## Step 2 — Run the Transformer

```bash
python validate/adv-transform.py \
  --profile observation \
  --input my-data.csv \
  --output my-data.jsonld \
  --base-uri https://data.my-org.org/
```

The `--base-uri` flag sets the prefix for generated entity IRIs (e.g., `https://data.my-org.org/observation/MY-SENSOR-001`).

## Step 3 — Validate

```bash
python validate/adv-validate.py \
  --content my-data.jsonld \
  --content-only --profile observation
```

## Multiple Rows

If your CSV has multiple data rows, the transformer produces a JSON array. Each element is a valid ADV JSON-LD document.

## Common Issues

**"Missing column X"** — Your CSV headers don't match the template. Check `profiles/<profile>/csv-template.csv` for the exact column names.

**Geometry coordinates not valid** — The `geometryCoordinatesWGS84` column must contain a JSON array. Make sure it's quoted properly in the CSV.

**IRI columns** — Columns ending in `IRI` (like `observedProperty`, `cropSpeciesIRI`, `typeIRI`) must contain full URIs, not plain text. See `docs/VOCABULARY_GUIDE.md` for where to find the right IRIs.
