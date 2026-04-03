# ADAPT Standard to ADV Alignment Guide

This document maps concepts from the **AgGateway ADAPT Standard** (v2.0) to **ADV Data Model** profiles. It enables precision agriculture data produced in ADAPT format to be described, governed, and discovered in IDSA/DSP-compliant data spaces using ADV wrappers.

> **ADV does not replace ADAPT.** ADAPT excels at deep field-operation data (as-planted, as-applied, yield maps). ADV provides the governance and catalog layer that makes ADAPT datasets discoverable and policy-governed in European agricultural data spaces.

---

## Architecture: How They Work Together

```
┌──────────────────────────────────────────────────────────────┐
│                   DATA SPACE (DSP / IDSA)                    │
│                                                              │
│  ┌─────────────────────────┐   ┌──────────────────────────┐  │
│  │   ADV Governance Layer  │   │   ADAPT Data Payload     │  │
│  │   (dcat:Dataset wrapper)│   │   (JSON + GeoParquet)    │  │
│  │                         │   │                          │  │
│  │  dct:title              │   │  WorkRecord / Operation  │  │
│  │  adv:profileId          │──→│  CropZone / Field        │  │
│  │  odrl:hasPolicy         │   │  SpatialRecordsFile      │  │
│  │  dcat:distribution      │   │  Product / ProductMix    │  │
│  └─────────────────────────┘   └──────────────────────────┘  │
└──────────────────────────────────────────────────────────────┘
```

The ADV `dcat:Dataset` wrapper describes the ADAPT dataset for catalog discovery and attaches usage policies. The ADAPT payload itself travels as-is through the data space connector.

---

## Concept Mapping

### Structural Concepts

| ADAPT Concept | ADV Equivalent | Notes |
|--------------|----------------|-------|
| **Grower** | `dct:publisher` (in wrapper) | The data provider / agricultural producer |
| **Farm** | No direct equivalent | Organizational grouping; represented in wrapper metadata |
| **Field** | `saref4agri:Parcel` (Parcel-Crop profile) | A bounded area of land |
| **CropZone** | `saref4agri:Parcel` + `saref4agri:hasCrop` | A field area with a specific crop in a specific season |
| **WorkRecord** | `foodie:Intervention` (Intervention profile) | An operation performed on a field |
| **Operation** | `dct:type` within Intervention | A single activity (planting, spraying, harvesting) |
| **TimeScope** | `prov:startedAtTime` / `prov:endedAtTime` | Temporal bounds of the operation |
| **Product / ProductMix** | `prov:used` within Intervention | Inputs used in the operation |
| **SummaryValue** | `sosa:hasResult` / `qudt:numericValue` + `qudt:unit` | Aggregate totals for an operation |
| **SpatialRecordsFile** | `dcat:Distribution` (in wrapper) | GeoParquet file accessible via `dcat:accessURL` |
| **ReferenceLayer** | `dcat:Distribution` (in wrapper) | GeoTiff or GeoParquet reference data |

### Data Types

| ADAPT Data Type | ADV Profile | When to Use |
|----------------|-------------|-------------|
| Planting record | `adv.intervention` | As-planted data (variety, population, depth) |
| Application record | `adv.intervention` | As-applied data (fertilizer, chemicals, seed rates) |
| Harvest record | `adv.intervention` | Yield data (mass, moisture, area harvested) |
| Field boundary | `adv.parcel-crop` | Field or crop zone geometry |
| Soil sampling results | `adv.soil-analysis` | Lab results linked to sampling points |
| Weather station readings | `adv.weather-observation` | Meteorological data from on-farm stations |

### Units

ADAPT v2.0 uses its own Data Type Definitions for units. QUDT equivalents:

| ADAPT Unit | QUDT IRI |
|-----------|----------|
| kg | `http://qudt.org/vocab/unit/KiloGM` |
| kg/ha | `http://qudt.org/vocab/unit/KilogramPerHectare` |
| L/ha | `http://qudt.org/vocab/unit/LiterPerHectare` |
| seeds/ha | Use custom: `https://w3id.org/adv/vocab/unit/SeedsPerHectare` |
| bu/ac | `http://qudt.org/vocab/unit/BushelPerAcre` (North American) |
| ha | `http://qudt.org/vocab/unit/Hectare` |
| ac | `http://qudt.org/vocab/unit/Acre` |

---

## Wrapping an ADAPT Dataset for a Data Space

### Step 1: Choose the ADV profile

An ADAPT dataset typically contains one or more WorkRecords. Choose the ADV profile based on the dominant content:

- **Planting / Application / Harvest operations** -> `adv.intervention`
- **Field boundaries with crop info** -> `adv.parcel-crop`
- **Observation-style sensor data** -> `adv.observation`

### Step 2: Create the DCAT wrapper

```json
{
  "@context": {
    "dcat": "http://www.w3.org/ns/dcat#",
    "dct": "http://purl.org/dc/terms/",
    "odrl": "http://www.w3.org/ns/odrl/2/",
    "adv": "https://w3id.org/adv/core#",
    "xsd": "http://www.w3.org/2001/XMLSchema#"
  },

  "@type": "dcat:Dataset",
  "dct:title": "Corn harvest 2025 — Thompson Farm, Field North-40",
  "dct:description": "Yield map from combine harvest of corn (Zea mays), Sept 2025. Contains as-harvested GeoParquet with mass flow, moisture, and GPS coordinates.",
  "dct:identifier": "adapt-harvest-thompson-north40-2025",

  "adv:profileId": "adv.intervention",
  "adv:profileVersion": "1.0.0",
  "dct:conformsTo": { "@id": "https://w3id.org/adv/core#intervention-v1" },

  "dct:publisher": { "@id": "https://example.org/grower/thompson-farms" },
  "dct:issued": { "@value": "2025-10-05T12:00:00Z", "@type": "xsd:dateTime" },
  "dct:license": { "@id": "https://creativecommons.org/licenses/by/4.0/" },

  "dcat:distribution": [
    {
      "@type": "dcat:Distribution",
      "dcat:mediaType": "application/vnd.apache.parquet",
      "dcat:accessURL": { "@id": "https://data.thompson-farms.example/adapt/harvest/2025/north40.parquet" }
    },
    {
      "@type": "dcat:Distribution",
      "dcat:mediaType": "application/json",
      "dcat:accessURL": { "@id": "https://data.thompson-farms.example/adapt/harvest/2025/north40.json" }
    }
  ],

  "odrl:hasPolicy": {
    "@type": "odrl:Policy",
    "dct:title": "Research Only",
    "odrl:permission": {
      "@type": "odrl:Permission",
      "odrl:action": "http://www.w3.org/ns/odrl/2/use",
      "odrl:constraint": {
        "odrl:leftOperand": "http://www.w3.org/ns/odrl/2/purpose",
        "odrl:operator": "http://www.w3.org/ns/odrl/2/eq",
        "odrl:rightOperand": "https://w3id.org/dpv#ResearchAndDevelopment"
      }
    }
  }
}
```

### Step 3: Validate the wrapper

```bash
python validate/adv-validate.py \
  --wrapper my-adapt-offer.jsonld \
  --content my-adapt-summary.jsonld
```

> **Note:** The ADAPT GeoParquet payload is not validated by ADV SHACL (it is not RDF). The wrapper validation ensures the dataset self-description is correct for catalog discovery. If you also produce a JSON-LD summary of the operation, that can be validated against the Intervention profile shape.

---

## Key Differences

| Aspect | ADAPT | ADV |
|--------|-------|-----|
| **Purpose** | Field operation data exchange | Data space catalog + governance |
| **Format** | JSON + GeoParquet + GeoTiff | JSON-LD + Turtle (RDF) |
| **Semantics** | Custom JSON Schema | SOSA, SAREF4AGRI, FOODIE (OWL/RDF) |
| **Governance** | None | DCAT wrappers + ODRL policies |
| **Validation** | JSON Schema conformance | SHACL shape validation |
| **Geography** | North American focus | European data space focus |
| **Complementary** | Yes — ADAPT is the payload | Yes — ADV is the envelope |

---

## Further Reading

- [ADAPT Standard v2.0 Documentation](https://adaptstandard.org/docs/)
- [AgGateway ADAPT GitHub](https://github.com/ADAPT/Standard)
- ADV Intervention profile: `profiles/intervention/`
- ADV DCAT wrapper template: `offers/offer.template.jsonld`
