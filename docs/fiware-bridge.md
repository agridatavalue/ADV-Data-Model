# FIWARE Smart Data Models to ADV Bridge Guide

This guide shows how to take NGSI-LD entities from FIWARE AgriFood Smart Data Models and expose them as ADV-compliant datasets in an IDSA/DSP data space.

> **ADV does not replace FIWARE.** FIWARE provides the real-time IoT platform (context broker, IoT agents). ADV provides the semantic application profile that makes FIWARE data discoverable and policy-governed through IDSA connectors.

---

## Architecture

```
┌──────────────────────────────────────────────────────────────┐
│  FIWARE Platform                                             │
│  ┌──────────────┐   ┌──────────────┐   ┌──────────────────┐  │
│  │  IoT Agent   │──→│ Context      │──→│  ADV Adapter     │  │
│  │  (sensors)   │   │ Broker       │   │  (JSON-LD        │  │
│  └──────────────┘   │ (Orion-LD)   │   │   transform)     │  │
│                     └──────────────┘   └────────┬─────────┘  │
│                                                 │            │
│                                                 ▼            │
│                                        ┌────────────────┐    │
│                                        │ IDSA Connector │    │
│                                        │ (EDC / TRUE)   │    │
│                                        │                │    │
│                                        │ dcat:Dataset   │    │
│                                        │ + ADV profile  │    │
│                                        │ + ODRL policy  │    │
│                                        └────────────────┘    │
└──────────────────────────────────────────────────────────────┘
```

---

## Entity Mapping: FIWARE Smart Data Models -> ADV Profiles

| FIWARE Entity Type | ADV Profile | ADV Target Class |
|-------------------|-------------|------------------|
| `AgriParcel` | `adv.parcel-crop` | `saref4agri:Parcel` |
| `AgriParcelRecord` | `adv.observation` | `sosa:Observation` |
| `AgriParcelOperation` | `adv.intervention` | `foodie:Intervention` |
| `AgriCrop` | `adv.parcel-crop` (nested) | `saref4agri:Crop` |
| `Animal` | `adv.animal` | `saref4agri:Animal` |
| `WeatherObserved` | `adv.weather-observation` | `sosa:Observation` |

---

## Property Mapping

### AgriParcel -> ADV Parcel-Crop

| FIWARE Property | ADV Property | Notes |
|----------------|-------------|-------|
| `id` | `adv:externalId` | Extract local identifier from the NGSI-LD URN |
| `location` (GeoJSON) | `geo:hasGeometry` | Wrap in GeoJSON vocabulary format |
| `hasAgriCrop` | `saref4agri:hasCrop` | Reference to crop entity |
| `area` | `foodie:cropArea` | Numeric value in hectares |
| `dateCreated` | `adv:issuedAt` | Convert to xsd:dateTime |

**FIWARE NGSI-LD input:**
```json
{
  "id": "urn:ngsi-ld:AgriParcel:parcel-001",
  "type": "AgriParcel",
  "location": {
    "type": "GeoProperty",
    "value": { "type": "Polygon", "coordinates": [[[23.7, 37.9], [23.71, 37.9], [23.71, 37.91], [23.7, 37.91], [23.7, 37.9]]] }
  },
  "hasAgriCrop": { "type": "Relationship", "object": "urn:ngsi-ld:AgriCrop:wheat-2025" },
  "area": { "type": "Property", "value": 12.5 }
}
```

**ADV JSON-LD output:**
```json
{
  "@context": {
    "saref4agri": "https://saref.etsi.org/saref4agri/",
    "foodie": "http://foodie-cloud.com/model/foodie#",
    "geo": "http://www.opengis.net/ont/geosparql#",
    "adv": "https://w3id.org/adv/core#",
    "geojson": "https://purl.org/geojson/vocab#",
    "xsd": "http://www.w3.org/2001/XMLSchema#"
  },
  "@type": "saref4agri:Parcel",
  "adv:externalId": "parcel-001",
  "geo:hasGeometry": {
    "@type": "geojson:Polygon",
    "geojson:coordinates": [[[23.7, 37.9], [23.71, 37.9], [23.71, 37.91], [23.7, 37.91], [23.7, 37.9]]]
  },
  "saref4agri:hasCrop": {
    "@type": "saref4agri:Crop",
    "foodie:cropSpecies": { "@id": "http://aims.fao.org/aos/agrovoc/c_7951" }
  },
  "foodie:cropArea": { "@value": "12.5", "@type": "xsd:decimal" }
}
```

### AgriParcelRecord -> ADV Observation

| FIWARE Property | ADV Property | Notes |
|----------------|-------------|-------|
| `id` | `adv:externalId` | Extract local ID |
| `hasAgriParcel` | `sosa:hasFeatureOfInterest` | Reference to the parcel |
| `soilMoistureEC` / `soilTemperature` / etc. | `sosa:observedProperty` + `sosa:hasResult` | Map each measured quantity to a separate observation |
| `observedAt` (NGSI-LD temporal) | `sosa:resultTime` | Convert to xsd:dateTime |
| Device entity IRI | `sosa:madeBySensor` | Reference to the device |

### AgriParcelOperation -> ADV Intervention

| FIWARE Property | ADV Property | Notes |
|----------------|-------------|-------|
| `id` | `adv:externalId` | Extract local ID |
| `hasAgriParcel` | `sosa:hasFeatureOfInterest` | Target field |
| `operationType` | `dct:type` | Convert to IRI (use AGROVOC) |
| `startedAt` | `prov:startedAtTime` | xsd:dateTime |
| `endedAt` | `prov:endedAtTime` | xsd:dateTime |
| `hasAgriProductType` | `prov:used` | Input product reference |
| `quantity` / `waterSource` | `qudt:numericValue` + `qudt:unit` | Nested in `prov:used` |

### Animal -> ADV Animal

| FIWARE Property | ADV Property | Notes |
|----------------|-------------|-------|
| `id` | `adv:externalId` | Extract local ID |
| `species` | `adv:species` | Convert to IRI (use NCBI Taxonomy) |
| `birthdate` | `adv:birthDate` | xsd:date |
| `sex` | `adv:sex` | Convert to ADV vocabulary IRI (`adv:sex-male`, `adv:sex-female`) |
| `legalID` | `adv:externalId` | Prefer official registration ID |

### WeatherObserved -> ADV Weather Observation

| FIWARE Property | ADV Property | Notes |
|----------------|-------------|-------|
| `id` | `adv:externalId` | Extract local ID |
| `temperature` | `sosa:observedProperty` = `quantitykind:Temperature` | One observation per parameter |
| `relativeHumidity` | `sosa:observedProperty` = `quantitykind:RelativeHumidity` | One observation per parameter |
| `precipitation` | `sosa:observedProperty` = `quantitykind:Precipitation` | One observation per parameter |
| `windSpeed` | `sosa:observedProperty` = `quantitykind:WindSpeed` | One observation per parameter |
| `dateObserved` | `sosa:resultTime` | xsd:dateTime |
| `location` | `sosa:hasFeatureOfInterest` | Station or area |
| `stationCode` | `sosa:madeBySensor` | Station reference |

---

## Step-by-Step: Exposing FIWARE Data via ADV in a Data Space

### 1. Query the Context Broker

```bash
curl -H "Accept: application/ld+json" \
  http://localhost:1026/ngsi-ld/v1/entities?type=AgriParcel
```

### 2. Transform NGSI-LD to ADV JSON-LD

Use the mappings above. Key transformations:
- Extract local ID from NGSI-LD URN (`urn:ngsi-ld:AgriParcel:X` -> `X`)
- Unwrap NGSI-LD property wrappers (`{"type": "Property", "value": V}` -> `V`)
- Convert relationship objects to `@id` references
- Add `@type` from the ADV profile target class
- Apply the shared context: `model/adv-context.jsonld`

### 3. Create the DCAT Wrapper

Use `offers/offer.template.jsonld` and set:
- `adv:profileId` to the matching profile
- `dcat:accessURL` to the context broker endpoint or transformed data URL
- `odrl:hasPolicy` to your chosen policy template

### 4. Validate

```bash
python validate/adv-validate.py \
  --wrapper my-fiware-offer.jsonld \
  --content my-fiware-parcel.jsonld
```

### 5. Register in IDSA Connector

Load the validated wrapper into your EDC or TRUE Connector catalog. The dataset is now discoverable by any DSP-compliant consumer.

---

## JSON-LD Context for FIWARE-to-ADV

The shared ADV context (`model/adv-context.jsonld`) already includes all necessary prefix mappings. For FIWARE-specific short names, add these to your transformation context:

```json
{
  "@context": [
    "https://w3id.org/adv/context.jsonld",
    {
      "AgriParcel": "saref4agri:Parcel",
      "AgriCrop": "saref4agri:Crop",
      "AgriParcelOperation": "foodie:Intervention",
      "WeatherObserved": "sosa:Observation",
      "hasAgriCrop": "saref4agri:hasCrop",
      "hasAgriParcel": "sosa:hasFeatureOfInterest",
      "operationType": { "@id": "dct:type", "@type": "@id" },
      "area": { "@id": "foodie:cropArea", "@type": "xsd:decimal" },
      "soilMoistureEC": "sosa:hasResult"
    }
  ]
}
```

---

## Further Reading

- [FIWARE Smart Data Models — AgriFood](https://github.com/smart-data-models/dataModel.Agrifood)
- [NGSI-LD Specification (ETSI GS CIM 009)](https://www.etsi.org/deliver/etsi_gs/CIM/001_099/009/)
- ADV translator alignment notes: `docs/translator-alignment.md`
- ADV shared context: `model/adv-context.jsonld`
