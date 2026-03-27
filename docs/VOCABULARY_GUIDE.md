# ADV Data Model — Vocabulary Guide

Several ADV profile properties require **IRI values** — references to terms from external vocabularies rather than free text. This guide lists recommended vocabulary sources for each type of IRI field.

---

## Observed Properties (Observation Profile)

**Field:** `sosa:observedProperty`

| Source | Coverage | Example IRI |
|--------|----------|-------------|
| [QUDT Quantity Kinds](http://qudt.org/2.1/vocab/quantitykind) | Physical quantities (temperature, pressure, moisture) | `http://qudt.org/vocab/quantitykind/Temperature` |
| [AGROVOC](https://agrovoc.fao.org/) | Agriculture-specific terms (soil moisture, crop yield, pest incidence) | `http://aims.fao.org/aos/agrovoc/c_7154` (soil moisture) |
| Custom domain URIs | Project-specific phenomena | `https://data.your-domain.org/phenomenon/soilMoisture` |

---

## Units of Measurement

**Field:** `qudt:unit`

| Source | Coverage | Example IRI |
|--------|----------|-------------|
| [QUDT Units](http://qudt.org/2.1/vocab/unit) | Comprehensive unit catalog | `http://qudt.org/vocab/unit/DegreeCelsius` |
| | | `http://qudt.org/vocab/unit/VolumeFraction` |
| | | `http://qudt.org/vocab/unit/Hectare` |
| | | `http://qudt.org/vocab/unit/Liter` |
| | | `http://qudt.org/vocab/unit/KilogramPerHectare` |

QUDT is the recommended source for all units. Browse the full catalog at http://qudt.org/2.1/vocab/unit.

---

## Crop Types (Parcel-Crop Profile)

**Field:** `foodie:cropSpecies`

| Source | Coverage | Example IRI |
|--------|----------|-------------|
| [AGROVOC](https://agrovoc.fao.org/) | FAO multilingual agricultural thesaurus | `http://aims.fao.org/aos/agrovoc/c_7951` (wheat) |
| [EPPO Global Database](https://gd.eppo.int/) | Plant species codes (European standard) | `https://gd.eppo.int/taxon/TRZAX` (common wheat) |
| [Wikidata](https://www.wikidata.org/) | General-purpose linked data | `http://www.wikidata.org/entity/Q15645384` (common wheat) |

---

## Species (Animal Profile)

**Field:** `adv:species`

| Source | Coverage | Example IRI |
|--------|----------|-------------|
| [NCBI Taxonomy](https://www.ncbi.nlm.nih.gov/taxonomy) | Biological taxonomy (authoritative for species) | `http://purl.obolibrary.org/obo/NCBITaxon_9913` (Bos taurus) |
| [Wikidata](https://www.wikidata.org/) | General-purpose linked data | `http://www.wikidata.org/entity/Q830` (cattle) |
| [AGROVOC](https://agrovoc.fao.org/) | Agricultural species | `http://aims.fao.org/aos/agrovoc/c_927` (cattle) |

---

## Activity / Intervention Types

**Field:** `dct:type` (Intervention Profile)

| Source | Coverage | Example IRI |
|--------|----------|-------------|
| [AGROVOC](https://agrovoc.fao.org/) | Agricultural operations | `http://aims.fao.org/aos/agrovoc/c_7173` (spraying) |
| [INSPIRE code lists](https://inspire.ec.europa.eu/codelist) | EU spatial data infrastructure | Activity-specific code lists |
| Custom domain URIs | Project-specific operations | `https://data.your-domain.org/activity/Spraying` |

---

## Alert Types

**Field:** `dct:type` (Alert Profile)

| Source | Coverage | Example IRI |
|--------|----------|-------------|
| [AGROVOC](https://agrovoc.fao.org/) | Pest and disease terms | `http://aims.fao.org/aos/agrovoc/c_5728` (pests) |
| [EPPO Global Database](https://gd.eppo.int/) | Pest organism codes | `https://gd.eppo.int/taxon/MYZUPE` (green peach aphid) |
| Custom domain URIs | Domain-specific alert categories | `https://data.your-domain.org/alertType/Pest` |

---

## Severity Levels

**Field:** `adv:severity`

No single standard vocabulary exists for severity. Common approaches:

| Approach | Example IRIs |
|----------|-------------|
| Simple 3-level scale | `https://w3id.org/adv/vocab/severity/Low`, `Medium`, `High` |
| CAP (Common Alerting Protocol) | `urn:oasis:names:tc:emergency:cap:1.2:severity:Minor` |
| Custom domain | `https://data.your-domain.org/severity/Critical` |

---

## Sex / Gender (Animal Profile)

**Field:** `adv:sex`

| Approach | Example IRIs |
|----------|-------------|
| Simple vocabulary | `https://w3id.org/adv/vocab/sex/Male`, `Female` |
| Schema.org | `https://schema.org/Male`, `https://schema.org/Female` |
| Wikidata | `http://www.wikidata.org/entity/Q44148` (male), `Q43445` (female) |

---

## Production Types (Animal Profile)

**Field:** `adv:productionType`

No single standard. Common values:

| Value | Suggested IRI |
|-------|--------------|
| Dairy | `https://w3id.org/adv/vocab/productionType/Dairy` |
| Meat | `https://w3id.org/adv/vocab/productionType/Meat` |
| Egg | `https://w3id.org/adv/vocab/productionType/Egg` |
| Wool | `https://w3id.org/adv/vocab/productionType/Wool` |

---

## General Advice

1. **Prefer established vocabularies** (AGROVOC, QUDT, EPPO) over custom IRIs.
2. **Use AGROVOC as the default** for agricultural terms — it's multilingual, maintained by FAO, and widely adopted.
3. **For units, always use QUDT** — it's the most comprehensive and interoperable unit vocabulary.
4. **If you must create custom IRIs**, use a stable base URI under your domain and document the terms.
5. **IRIs don't need to resolve** during development, but they should be stable identifiers. Plan for resolution when publishing.
