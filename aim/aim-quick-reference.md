# AIM Quick Reference for ADV Users

This is a **practical cheat sheet** for the parts of the Agriculture Information Model (AIM) used by the ADV Data Model.  
It’s written for implementers who only need to understand which AIM classes and properties appear in the ADV profiles.

---

## 🎯 Core AIM Classes Used by ADV

| AIM Class (IRI) | Used In ADV Profile | Meaning |
|-----------------|---------------------|----------|
| `aim:Observation` | Observation | A measurement or estimation made by a sensor or process. |
| `aim:FeatureOfInterest` | Observation, Parcel-Crop | The feature being observed or managed (e.g. field, plot, area). |
| `aim:Activity` | Intervention | A field operation or management activity. |
| `aim:Animal` | Animal | An animal, identified and described by species, birth, etc. |
| `aim:Alert` | Alert | A notification or advisory event affecting a target feature. |

---

## ⚙️ Common AIM Properties

| Property | Applies To | Description | Example |
|-----------|-------------|-------------|----------|
| `aim:resultTime` *(xsd:dateTime)* | Observation | When the result is valid. | `2025-09-21T10:35:00Z` |
| `aim:observedProperty` *(IRI)* | Observation | What was measured or observed. | `https://w3id.org/phenomenon/soilMoisture` |
| `aim:madeBySensor` *(IRI)* | Observation | The sensor or instrument that produced the result. | `https://data.example.org/sensor/SM-10` |
| `aim:hasFeatureOfInterest` *(IRI)* | Observation, Activity, Alert | The thing or location being observed, acted on, or affected. | `https://data.example.org/parcel/field-a` |
| `aim:hasResult → aim:result → aim:value` *(xsd:decimal)* | Observation | The numeric result of a measurement. | `0.23` |
| `aim:hasResult → aim:result → aim:unit` *(IRI)* | Observation | The unit of measure (use QUDT IRI). | `unit:VolumeFraction` |
| `aim:activityType` *(IRI)* | Activity | Type of operation or action performed. | `https://w3id.org/activity/Spraying` |
| `aim:startTime`, `aim:endTime` *(xsd:dateTime)* | Activity, Alert | Start and end of an event or activity. | `2025-04-10T06:30:00Z` |
| `aim:alertType`, `aim:severity` *(IRI)* | Alert | Category and severity of alert. | `…/Pest`, `…/High` |
| `aim:species` *(IRI)* | Animal | Biological species of the animal. | `https://w3id.org/species/Bos_taurus` |
| `aim:birthDate` *(xsd:date)* | Animal | Animal’s date of birth. | `2021-03-14` |

---

## 🧩 How to Use AIM in ADV

- **You don’t need to import the full AIM ontology manually.**  
  ADV SHACL files already reference AIM classes. Just fill the JSON-LD templates.

- **If you need more AIM properties** (e.g. for extended metadata),  
  add them using the same namespace (`https://w3id.org/aim#`).  
  SHACL validation will accept additional properties beyond the required ones.

- **Always use IRIs instead of plain strings** for things like crop type, operation type, or unit — this keeps data interoperable.

---

## 📘 Version and Reference

ADV Data Model v1.1 is aligned with:

- **AIM release:** current master (as of October 2025)  
- **Namespace root:** `https://w3id.org/aim#`  
- **Official repository:** https://github.com/AgricultureInformationModel/AIM  

---

## 🔗 When You Need AIM Locally

For tools that require a local import, see the accompanying file  
`pinned-import.ttl`, which points to the same official AIM ontology.  
You can use it as an entry point in editors, validators, or pipelines.
