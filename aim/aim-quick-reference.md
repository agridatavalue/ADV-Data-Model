# AIM Quick Reference for ADV Users

This is a **practical cheat sheet** for the parts of the Agriculture Information Model (AIM) used by the ADV Data Model v2.0.
It's written for implementers who only need to understand which upstream classes and properties appear in the ADV profiles.

---

## Upstream Vocabulary Sources

ADV v2.0 uses terms from these established standards (all part of the AIM vocabulary stack):

| Prefix | Namespace | Standard |
|--------|-----------|----------|
| `sosa:` | `http://www.w3.org/ns/sosa/` | W3C Sensor, Observation, Sample, and Actuator |
| `geo:` | `http://www.opengis.net/ont/geosparql#` | OGC GeoSPARQL |
| `saref4agri:` | `https://saref.etsi.org/saref4agri/` | ETSI SAREF for Agriculture |
| `foodie:` | `http://foodie-cloud.com/model/foodie#` | FOODIE ontology (via DEMETER/AIM) |
| `qudt:` | `http://qudt.org/schema/qudt/` | QUDT Quantities, Units, Dimensions |
| `prov:` | `http://www.w3.org/ns/prov#` | W3C Provenance Ontology |
| `schema:` | `https://schema.org/` | Schema.org |
| `dct:` | `http://purl.org/dc/terms/` | Dublin Core Terms |
| `dcat:` | `http://www.w3.org/ns/dcat#` | W3C Data Catalog Vocabulary |
| `odrl:` | `http://www.w3.org/ns/odrl/2/` | W3C ODRL (usage policies) |

---

## Core Classes Used by ADV

| Class (full IRI) | Used In ADV Profile | Meaning |
|-------------------|---------------------|---------|
| `sosa:Observation` | Observation | A measurement or estimation made by a sensor or process. |
| `sosa:FeatureOfInterest` | Observation, Intervention, Alert | The feature being observed or managed (e.g., field, plot, area). |
| `sosa:Sensor` | Observation | The device or process that produced the observation. |
| `saref4agri:Parcel` | Parcel-Crop | An agricultural parcel, field, or plot. |
| `saref4agri:Crop` | Parcel-Crop | A crop instance associated with a parcel. |
| `saref4agri:Animal` | Animal | An animal, identified and described by species, birth, etc. |
| `foodie:Intervention` | Intervention | A field operation or management activity. |
| `foodie:Alert` | Alert | A notification or advisory event affecting a target feature. |
| `dcat:Dataset` | Wrapper (all profiles) | The dataset self-description for data space exchange. |

---

## Common Properties by Profile

### Observation Profile
| Property | Namespace | Description | Example |
|----------|-----------|-------------|---------|
| `sosa:resultTime` | W3C SOSA | When the result is valid | `2025-09-21T10:35:00Z` |
| `sosa:observedProperty` | W3C SOSA | What was measured (IRI) | `https://w3id.org/phenomenon/soilMoisture` |
| `sosa:madeBySensor` | W3C SOSA | The sensor that produced the result | `https://data.example.org/sensor/SM-10` |
| `sosa:hasFeatureOfInterest` | W3C SOSA | The location or thing observed | `https://data.example.org/parcel/field-a` |
| `sosa:hasResult` | W3C SOSA | The result node (contains value + unit) | — |
| `qudt:numericValue` | QUDT | The numeric measurement value | `0.23` |
| `qudt:unit` | QUDT | The unit of measure (IRI) | `unit:VolumeFraction` |

### Parcel-Crop Profile
| Property | Namespace | Description | Example |
|----------|-----------|-------------|---------|
| `geo:hasGeometry` | OGC GeoSPARQL | The parcel's spatial geometry | GeoJSON Polygon |
| `saref4agri:hasCrop` | ETSI SAREF4AGRI | Link to a crop instance | — |
| `foodie:cropSpecies` | FOODIE | IRI to crop species | `https://w3id.org/crop/Wheat` |
| `foodie:cropArea` | FOODIE | Area in hectares | `2.45` |

### Intervention Profile
| Property | Namespace | Description | Example |
|----------|-----------|-------------|---------|
| `dct:type` | Dublin Core | Type of operation (IRI) | `https://w3id.org/activity/Spraying` |
| `prov:startedAtTime` | W3C PROV | Start time | `2025-04-10T06:30:00Z` |
| `prov:endedAtTime` | W3C PROV | End time | `2025-04-10T07:45:00Z` |
| `sosa:hasFeatureOfInterest` | W3C SOSA | The target parcel | — |
| `prov:used` | W3C PROV | Input material/product | — |
| `prov:generated` | W3C PROV | Output product/result | — |

### Animal Profile
| Property | Namespace | Description | Example |
|----------|-----------|-------------|---------|
| `schema:species` | Schema.org | Biological species (IRI) | `https://w3id.org/species/Bos_taurus` |
| `schema:birthDate` | Schema.org | Date of birth | `2021-03-14` |
| `schema:gender` | Schema.org | Sex (IRI) | `https://w3id.org/vocab/sex/Female` |
| `adv:productionType` | ADV | Production type (IRI) | `https://w3id.org/vocab/productionType/Dairy` |
| `adv:hasParent` | ADV | Link to parent animal | — |

### Alert Profile
| Property | Namespace | Description | Example |
|----------|-----------|-------------|---------|
| `dct:type` | Dublin Core | Alert category (IRI) | `https://w3id.org/alertType/Pest` |
| `adv:severity` | ADV | Severity level (IRI) | `https://w3id.org/severity/High` |
| `dct:description` | Dublin Core | Human-readable message | "Aphid risk detected..." |
| `sosa:hasFeatureOfInterest` | W3C SOSA | Affected location/entity | — |
| `prov:startedAtTime` | W3C PROV | When the alert became active | `2025-06-02T08:00:00Z` |
| `prov:endedAtTime` | W3C PROV | When the alert expired | `2025-06-05T18:00:00Z` |

---

## How to Use AIM in ADV

- **You don't need to install the full AIM ontology.** ADV SHACL shapes already reference the correct upstream URIs. Just fill the JSON-LD templates.

- **For JSON-LD producers**, use the ADV context file (`model/adv-context.jsonld`) which maps short names to the correct upstream URIs.

- **If you need more properties** (e.g., for extended metadata), add them from the same upstream vocabularies (SOSA, SAREF4AGRI, FOODIE, etc.). SHACL validation will accept additional properties beyond the required ones.

- **Always use IRIs instead of plain strings** for things like crop type, operation type, species, or unit.

---

## Version and Reference

ADV Data Model v2.0 is aligned with:

- **AIM (DEMETER/OGC SWG):** Uses actual AIM-aligned upstream URIs from SOSA, GeoSPARQL, SAREF4AGRI, and FOODIE.
- **IDSA Dataspace Protocol:** Wrapper layer uses DCAT vocabulary with ODRL policies.
- **Official AIM repository:** https://github.com/opengeospatial/aim-swg

---

## When You Need AIM Locally

For tools that require a local import, see the accompanying file
`pinned-import.ttl`, which points to the DEMETER aggregated ontology.
You can use it as an entry point in editors, validators, or pipelines.
