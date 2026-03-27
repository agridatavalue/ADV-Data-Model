# Translator Alignment (NGSI-LD / DEMETER -> ADV Profiles)

Some partners use NGSI-LD/DEMETER-shaped payloads. This note shows quick correspondences to ADV v2.0.

---

## Observation (NGSI-LD -> ADV Observation)
- NGSI-LD `observedAt` -> `sosa:resultTime`
- NGSI-LD `sensor`/device entity IRI -> `sosa:madeBySensor` `@id`
- NGSI-LD property IRI (e.g., `batteryLevel`) -> `sosa:observedProperty`
- NGSI-LD numeric value -> `sosa:hasResult` / `qudt:numericValue` (xsd:decimal)
- NGSI-LD unit (if present) -> `sosa:hasResult` / `qudt:unit` (QUDT IRI)

## Parcel (NGSI-LD -> ADV Parcel-Crop)
- NGSI-LD geometry `Point/Polygon` (WKT or coordinates) -> `geo:hasGeometry` (GeoJSON vocab in template)
- Local code/identifier -> `adv:externalId`
- Crop species -> `saref4agri:hasCrop` / `foodie:cropSpecies` (IRI)

## Intervention (NGSI-LD -> ADV Intervention)
- NGSI-LD activity type -> `dct:type` (IRI)
- NGSI-LD start/end time -> `prov:startedAtTime` / `prov:endedAtTime`
- NGSI-LD target field -> `sosa:hasFeatureOfInterest`
- NGSI-LD inputs/outputs -> `prov:used` / `prov:generated`

## Animal (NGSI-LD -> ADV Animal)
- NGSI-LD species -> `schema:species` (IRI)
- NGSI-LD birthdate -> `schema:birthDate` (xsd:date)
- NGSI-LD identifier -> `adv:externalId`

## Alert (NGSI-LD -> ADV Alert)
- NGSI-LD alert category -> `dct:type` (IRI)
- NGSI-LD severity -> `adv:severity` (IRI)
- NGSI-LD message -> `dct:description`
- NGSI-LD affected area -> `sosa:hasFeatureOfInterest`

---

> **Tip:** Start from `profiles/*/content.template.jsonld` and map your NGSI-LD keys to those fields.
> If you need help, place a small adapter between your NGSI-LD output and the ADV JSON-LD templates.
> The shared context file `model/adv-context.jsonld` provides all necessary prefix mappings.
