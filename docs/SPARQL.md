# ADV Data Model — SPARQL Queries (v1.0)

These SPARQL queries help you **validate**, **inspect**, and **govern** data modeled with the **AgriDataValue (ADV) Data Model**, which extends **AIM** with FAIR and dataspace semantics.

---

## 🧭 How to Use

- Each section title describes the purpose of the query (e.g. “CAP indicators missing evidence links”).  
- Copy the SPARQL statements below directly into your SPARQL editor or triplestore console (GraphDB, Fuseki, Stardog, etc.).  
- Before running, make sure you have loaded:
  - `model/adv.ttl` (the ontology)
  - `model/shapes.ttl` (for validation)

---

## 🧱 Prefixes (copy once)

PREFIX adv:  <https://w3id.org/adv#>  
PREFIX aim:  <https://w3id.org/ogc/aim#>  
PREFIX dcat: <http://www.w3.org/ns/dcat#>  
PREFIX dct:  <http://purl.org/dc/terms/>  
PREFIX prov: <http://www.w3.org/ns/prov#>  
PREFIX odrl: <http://www.w3.org/ns/odrl/2/>  
PREFIX sosa: <http://www.w3.org/ns/sosa/>  
PREFIX geo:  <http://www.opengis.net/ont/geosparql#>  
PREFIX qudt: <http://qudt.org/schema/qudt/>  
PREFIX xsd:  <http://www.w3.org/2001/XMLSchema#>

---

## ✅ FAIR / Quality Validation

### Datasets missing required FAIR metadata

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

### Observations missing unit or value

SELECT ?obs WHERE {  
  ?obs a sosa:Observation .  
  FILTER NOT EXISTS { ?obs qudt:unit ?unit }  
  UNION  
  FILTER NOT EXISTS { ?obs qudt:numericValue ?val }  
}

### Fields without geometry

SELECT ?field WHERE {  
  ?field a adv:Field .  
  FILTER NOT EXISTS { ?field geo:hasGeometry ?g }  
}

---

## 🔍 Discovery & Browsing

### List all datasets with key FAIR info

SELECT ?dataset ?title ?publisher ?license WHERE {  
  ?dataset a dcat:Dataset ;  
           dct:title ?title ;  
           dct:publisher ?publisher ;  
           dct:license ?license .  
}  
ORDER BY LCASE(STR(?title))

### List all observations for a specific field

SELECT ?obs ?prop ?val ?unit ?time WHERE {  
  VALUES (?field) { (<urn:field:1>) }   # Change to your field IRI  
  ?obs a sosa:Observation ;  
       sosa:hasFeatureOfInterest ?field ;  
       sosa:observedProperty ?prop ;  
       qudt:numericValue ?val ;  
       qudt:unit ?unit ;  
       sosa:resultTime ?time .  
}  
ORDER BY ?time

### All observed properties across fields

SELECT DISTINCT ?prop WHERE {  
  ?obs a sosa:Observation ;  
       sosa:hasFeatureOfInterest ?field ;  
       sosa:observedProperty ?prop .  
  ?field a adv:Field .  
}  
ORDER BY LCASE(STR(?prop))

---

## 🛡️ Governance & Usage Control

### Datasets and their ODRL policies

SELECT ?dataset ?policy ?title WHERE {  
  ?dataset a dcat:Dataset ;  
           odrl:hasPolicy ?policy .  
  ?policy a odrl:Policy ;  
          dct:title ?title .  
}  
ORDER BY LCASE(STR(?title))

### Datasets with IDS-style contract offers

SELECT ?dataset ?contract WHERE {  
  ?dataset a dcat:Dataset ;  
           adv:hasContract ?contract .  
}

### Policies allowing analysis but prohibiting distribution

SELECT DISTINCT ?policy WHERE {  
  ?policy a odrl:Policy ;  
          odrl:permission [ odrl:action odrl:analyze ] ;  
          odrl:prohibition [ odrl:action odrl:distribute ] .  
}

---

## 🛰️ Earth Observation (EO)

### EO products with high cloud cover (> 50%)

SELECT ?product ?cover WHERE {  
  ?product a adv:EOProduct ;  
           adv:cloudCover ?cover .  
  FILTER (xsd:decimal(?cover) > 50)  
}  
ORDER BY DESC(xsd:decimal(?cover))

### EO products linked to fields

# Adapt this to your linking strategy (e.g., spatial intersection, metadata join)  
SELECT ?product ?field WHERE {  
  ?product a adv:EOProduct .  
  ?field a adv:Field .  
  # Example: ?product adv:coversField ?field .  
}

---

## 🇪🇺 CAP Indicators

### CAP indicators justified by observations in 2025

SELECT ?indicator ?code ?obs ?time WHERE {  
  ?indicator a adv:CAPIndicator ;  
             adv:code ?code ;  
             adv:justifiedBy ?obs .  
  ?obs a sosa:Observation ;  
       sosa:resultTime ?time .  
  FILTER (?time >= "2025-01-01T00:00:00Z"^^xsd:dateTime &&  
          ?time <= "2025-12-31T23:59:59Z"^^xsd:dateTime)  
}  
ORDER BY ?code ?time

### CAP indicators missing evidence links

SELECT ?indicator WHERE {  
  ?indicator a adv:CAPIndicator .  
  FILTER NOT EXISTS { ?indicator adv:justifiedBy ?evidence }  
}

---

## 🌿 AIM Integration Checks

### Fields typed as both AIM and ADV

SELECT ?field WHERE {  
  ?field a adv:Field , aim:AgriParcel .  
}

### Datasets that publish AIM data

SELECT DISTINCT ?dataset WHERE {  
  ?dataset a dcat:Dataset .  
  ?thing a aim:AgriParcel .  
  # Adjust the linkage depending on how your dataset relates to AIM entities  
  # ?thing prov:wasDerivedFrom ?dataset .  
}

---

## 🧪 Debugging / Statistics

### Class count summary

SELECT ?type (COUNT(*) AS ?count) WHERE {  
  ?s a ?type .  
}  
GROUP BY ?type  
ORDER BY DESC(?count)

### Observations missing time or value

SELECT ?obs WHERE {  
  ?obs a sosa:Observation .  
  FILTER ( !EXISTS { ?obs sosa:resultTime ?t } ||  
           !EXISTS { ?obs qudt:numericValue ?v } )  
}

---

## 💡 Notes
- Run these queries after loading `model/adv.ttl` and `model/shapes.ttl`.  
- Queries are grouped by theme: FAIR, Governance, EO, CAP, AIM interop, Debug.  
- You can adjust time ranges, IRIs, or filters as needed.  
- For spatial linking (EO ↔ Fields), enable GeoSPARQL functions like `geof:sfIntersects` in your triplestore.  

✅ These queries are directly usable in GraphDB, Fuseki, Stardog, Virtuoso, and any SPARQL 1.1-compliant endpoint.
