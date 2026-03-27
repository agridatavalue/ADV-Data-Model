# NGSI-LD / FIWARE to ADV JSON-LD

Partners using NGSI-LD (e.g., through FIWARE, DEMETER toolbox, or Smart Data Models) can transform their payloads into ADV profiles.

## Conceptual Mapping

NGSI-LD and ADV serve different purposes:
- **NGSI-LD** is a context broker API format for real-time entity updates.
- **ADV** is a data space exchange format for dataset-level sharing with governance.

The transformation extracts domain content from NGSI-LD entities and re-packages it as ADV profile payloads with DCAT wrappers.

## Observation (NGSI-LD → ADV)

### NGSI-LD input (typical)
```json
{
  "id": "urn:ngsi-ld:SoilMoisture:SM-10-2025-09-21",
  "type": "SoilMoisture",
  "observedAt": "2025-09-21T10:35:00Z",
  "soilMoisture": {
    "type": "Property",
    "value": 0.23,
    "unitCode": "C62",
    "observedAt": "2025-09-21T10:35:00Z"
  },
  "location": {
    "type": "GeoProperty",
    "value": { "type": "Point", "coordinates": [3.7455, 51.0188] }
  },
  "refDevice": {
    "type": "Relationship",
    "object": "urn:ngsi-ld:Device:SM-10"
  }
}
```

### Mapping

| NGSI-LD field | ADV property | Notes |
|--------------|-------------|-------|
| `id` | `adv:externalId` | Strip `urn:ngsi-ld:` prefix or use as-is |
| `observedAt` (top-level) | `sosa:resultTime` | Use `{"@value": "...", "@type": "xsd:dateTime"}` |
| Property key (e.g., `soilMoisture`) | `sosa:observedProperty` | Map to a vocabulary IRI (AGROVOC, QUDT QuantityKind) |
| Property `value` | `qudt:numericValue` | Use `{"@value": "0.23", "@type": "xsd:decimal"}` |
| Property `unitCode` | `qudt:unit` | Map CEFACT unit code to QUDT IRI |
| `refDevice.object` | `sosa:madeBySensor` | Use `{"@id": "..."}` |
| `location.value` | `sosa:hasFeatureOfInterest` | Create or reference a FeatureOfInterest IRI |

### ADV output
```json
{
  "@context": { "sosa": "http://www.w3.org/ns/sosa/", "...": "..." },
  "@type": "sosa:Observation",
  "sosa:resultTime": { "@value": "2025-09-21T10:35:00Z", "@type": "xsd:dateTime" },
  "sosa:observedProperty": { "@id": "http://qudt.org/vocab/quantitykind/VolumeFraction" },
  "sosa:madeBySensor": { "@id": "urn:ngsi-ld:Device:SM-10", "@type": "sosa:Sensor" },
  "sosa:hasFeatureOfInterest": { "@id": "https://data.example.org/parcel/field-a", "@type": "sosa:FeatureOfInterest" },
  "sosa:hasResult": {
    "qudt:numericValue": { "@value": "0.23", "@type": "xsd:decimal" },
    "qudt:unit": { "@id": "http://qudt.org/vocab/unit/VolumeFraction" }
  },
  "adv:externalId": "SM-10-2025-09-21"
}
```

## Parcel / AgriParcel (NGSI-LD → ADV)

| NGSI-LD field | ADV property |
|--------------|-------------|
| `id` | `adv:externalId` |
| `location.value` (Polygon) | `geo:hasGeometry` |
| `hasAgriCrop.object` | `saref4agri:hasCrop` → `foodie:cropSpecies` |
| `area.value` | `foodie:cropArea` |

## Animal (NGSI-LD → ADV)

| NGSI-LD field | ADV property |
|--------------|-------------|
| `id` | `adv:externalId` |
| `species.value` | `adv:species` (map to taxonomy IRI) |
| `birthdate.value` | `adv:birthDate` |
| `sex.value` | `adv:sex` (map to IRI) |

## Unit Code Mapping (CEFACT → QUDT)

NGSI-LD often uses UN/CEFACT unit codes. Common mappings:

| CEFACT | QUDT IRI | Meaning |
|--------|----------|---------|
| `CEL` | `http://qudt.org/vocab/unit/DegreeCelsius` | Celsius |
| `C62` | (dimensionless — use `http://qudt.org/vocab/unit/VolumeFraction` for moisture) | Count |
| `LTR` | `http://qudt.org/vocab/unit/Liter` | Litre |
| `KGM` | `http://qudt.org/vocab/unit/Kilogram` | Kilogram |
| `HAR` | `http://qudt.org/vocab/unit/Hectare` | Hectare |
| `MTR` | `http://qudt.org/vocab/unit/Meter` | Metre |

## Implementation Options

1. **Manual** — Read this guide, transform your data by hand or with a script.
2. **CSV intermediary** — Export NGSI-LD entities to CSV matching the ADV template columns, then use `validate/adv-transform.py`.
3. **Custom adapter** — Write a small Python/JS script that reads NGSI-LD JSON and produces ADV JSON-LD. The mapping tables above are the specification.

In all cases, validate the output:
```bash
python validate/adv-validate.py --content output.jsonld --content-only --profile observation
```
