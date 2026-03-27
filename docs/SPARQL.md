# ADV Data Model — SPARQL Queries (v2.0)

These SPARQL queries help you **validate**, **inspect**, and **govern** data modeled with the **AgriDataValue (ADV) Data Model v2.0**, which uses upstream AIM vocabularies with DCAT/ODRL governance.

---

## How to Use

- Each section title describes the purpose of the query.
- Copy the SPARQL statements below directly into your SPARQL editor or triplestore console (GraphDB, Fuseki, Stardog, etc.).
- Before running, make sure you have loaded your ADV-compliant data and (optionally) the ADV ontology (`model/adv-core.ttl`).

---

## Prefixes (copy once)

```sparql
PREFIX adv:        <https://w3id.org/adv/core#>
PREFIX sosa:       <http://www.w3.org/ns/sosa/>
PREFIX geo:        <http://www.opengis.net/ont/geosparql#>
PREFIX saref4agri: <https://saref.etsi.org/saref4agri/>
PREFIX foodie:     <http://foodie-cloud.com/model/foodie#>
PREFIX qudt:       <http://qudt.org/schema/qudt/>
PREFIX prov:       <http://www.w3.org/ns/prov#>
PREFIX schema:     <https://schema.org/>
PREFIX dcat:       <http://www.w3.org/ns/dcat#>
PREFIX dct:        <http://purl.org/dc/terms/>
PREFIX odrl:       <http://www.w3.org/ns/odrl/2/>
PREFIX xsd:        <http://www.w3.org/2001/XMLSchema#>
```

---

## FAIR / Quality Validation

### Datasets missing required FAIR metadata

```sparql
SELECT ?dataset WHERE {
  ?dataset a dcat:Dataset .
  FILTER NOT EXISTS { ?dataset dct:title ?t }
  UNION
  FILTER NOT EXISTS { ?dataset dct:description ?d }
  UNION
  FILTER NOT EXISTS { ?dataset dct:publisher ?p }
  UNION
  FILTER NOT EXISTS { ?dataset dct:license ?lic }
  UNION
  FILTER NOT EXISTS { ?dataset dcat:distribution ?dist }
}
```

### Observations missing unit or value

```sparql
SELECT ?obs WHERE {
  ?obs a sosa:Observation .
  FILTER NOT EXISTS { ?obs sosa:hasResult ?r . ?r qudt:unit ?unit }
  UNION
  FILTER NOT EXISTS { ?obs sosa:hasResult ?r . ?r qudt:numericValue ?val }
}
```

### Parcels without geometry

```sparql
SELECT ?parcel WHERE {
  ?parcel a saref4agri:Parcel .
  FILTER NOT EXISTS { ?parcel geo:hasGeometry ?g }
}
```

---

## Discovery and Browsing

### List all datasets with key FAIR info

```sparql
SELECT ?dataset ?title ?publisher ?license WHERE {
  ?dataset a dcat:Dataset ;
           dct:title ?title ;
           dct:publisher ?publisher ;
           dct:license ?license .
}
ORDER BY LCASE(STR(?title))
```

### List all observations for a specific parcel

```sparql
SELECT ?obs ?prop ?val ?unit ?time WHERE {
  VALUES (?parcel) { (<urn:parcel:field-a>) }
  ?obs a sosa:Observation ;
       sosa:hasFeatureOfInterest ?parcel ;
       sosa:observedProperty ?prop ;
       sosa:hasResult ?r ;
       sosa:resultTime ?time .
  ?r qudt:numericValue ?val ;
     qudt:unit ?unit .
}
ORDER BY ?time
```

### All observed properties across parcels

```sparql
SELECT DISTINCT ?prop WHERE {
  ?obs a sosa:Observation ;
       sosa:hasFeatureOfInterest ?parcel ;
       sosa:observedProperty ?prop .
  ?parcel a saref4agri:Parcel .
}
ORDER BY LCASE(STR(?prop))
```

---

## Governance and Usage Control

### Datasets and their ODRL policies

```sparql
SELECT ?dataset ?policy ?title WHERE {
  ?dataset a dcat:Dataset ;
           odrl:hasPolicy ?policy .
  ?policy a odrl:Policy ;
          dct:title ?title .
}
ORDER BY LCASE(STR(?title))
```

### Datasets with ADV profile references

```sparql
SELECT ?dataset ?profileId ?profileVersion ?conformsTo WHERE {
  ?dataset a dcat:Dataset ;
           adv:profileId ?profileId ;
           adv:profileVersion ?profileVersion .
  OPTIONAL { ?dataset dct:conformsTo ?conformsTo }
}
```

### Policies allowing analysis but prohibiting distribution

```sparql
SELECT DISTINCT ?policy WHERE {
  ?policy a odrl:Policy ;
          odrl:permission [ odrl:action odrl:analyze ] ;
          odrl:prohibition [ odrl:action odrl:distribute ] .
}
```

---

## Domain-Specific Queries

### Interventions on a parcel in a date range

```sparql
SELECT ?intervention ?type ?start ?end WHERE {
  VALUES (?parcel) { (<urn:parcel:field-a>) }
  ?intervention a foodie:Intervention ;
                dct:type ?type ;
                prov:startedAtTime ?start ;
                prov:endedAtTime ?end ;
                sosa:hasFeatureOfInterest ?parcel .
  FILTER (?start >= "2025-01-01T00:00:00Z"^^xsd:dateTime &&
          ?end <= "2025-12-31T23:59:59Z"^^xsd:dateTime)
}
ORDER BY ?start
```

### Active alerts by severity

```sparql
SELECT ?alert ?type ?severity ?description ?start WHERE {
  ?alert a foodie:Alert ;
         dct:type ?type ;
         adv:severity ?severity ;
         dct:description ?description ;
         prov:startedAtTime ?start .
}
ORDER BY ?severity ?start
```

### Animals by species

```sparql
SELECT ?animal ?species ?birthDate WHERE {
  ?animal a saref4agri:Animal ;
          schema:species ?species ;
          schema:birthDate ?birthDate .
}
ORDER BY ?species ?birthDate
```

---

## Debugging / Statistics

### Class count summary

```sparql
SELECT ?type (COUNT(*) AS ?count) WHERE {
  ?s a ?type .
}
GROUP BY ?type
ORDER BY DESC(?count)
```

### Observations missing time or result

```sparql
SELECT ?obs WHERE {
  ?obs a sosa:Observation .
  FILTER ( !EXISTS { ?obs sosa:resultTime ?t } ||
           !EXISTS { ?obs sosa:hasResult ?r } )
}
```

---

## Notes
- Run these queries after loading your ADV-compliant data.
- Queries are grouped by theme: FAIR, Discovery, Governance, Domain, Debug.
- You can adjust time ranges, IRIs, or filters as needed.
- For spatial linking, enable GeoSPARQL functions like `geof:sfIntersects` in your triplestore.
