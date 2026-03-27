# Translator Alignment (NGSI-LD → ADV Profiles)

Some partners use NGSI-LD/DEMETER-shaped payloads. This note shows quick correspondences to ADV:

## Observation (NGSI-LD → ADV Observation)
- NGSI-LD `observedAt` → `aim:resultTime`
- NGSI-LD `sensor`/device entity IRI → `aim:madeBySensor` `@id`
- NGSI-LD property IRI (e.g., `batteryLevel`) → `aim:observedProperty`
- NGSI-LD numeric value → `aim:hasResult/aim:result/aim:value` (xsd:decimal)
- NGSI-LD unit (if present) → `aim:hasResult/aim:result/aim:unit` (QUDT IRI)

## Parcel (NGSI-LD → ADV Parcel-Crop)
- NGSI-LD geometry `Point/Polygon` (WKT or coordinates) → `aim:hasGeometry` (GeoJSON vocab in template)
- Local code/identifier → `adv:externalId`
- Crop species → `aim:hasCrop/aim:cropType` (IRI)

> Tip: Start from `profiles/*/content.template.jsonld` and map your NGSI-LD keys to those fields.  
> If you need help, place a small adapter between your NGSI-LD output and the ADV JSON-LD templates.
