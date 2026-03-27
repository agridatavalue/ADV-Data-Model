# AgriDataValue (ADV) Data Model  
**Version:** 1.1.0  
**Date:** 2025-10-31  

---

## Overview
The **AgriDataValue (ADV) Data Model** defines a practical and reusable structure for sharing agricultural data across data spaces.  
It combines three main standards:

1. **AIM – Agriculture Information Model** for domain semantics  
2. **IDS Information Model/Dataspace Protocol concepts** for data sharing metadata and interoperability  
3. **SHACL** for machine-readable validation  

The model provides a set of **five operational profiles** that cover the most common data exchange types in AgriDataValue and beyond.

---

## Included Profiles

| Profile | Purpose | Example Use Case |
|----------|----------|------------------|
| **Observation** | Sensor or Earth Observation measurements (time, value, unit) | Soil moisture, temperature |
| **Parcel-Crop** | Field and crop descriptions | Field boundaries, crop type |
| **Intervention** | Field operations or activities | Spraying, irrigation, fertilisation |
| **Animal** | Livestock and animal information | Animal identification, production events |
| **Alert** | Notifications and advisories | Pest or disease alerts, weather warnings |

Each profile folder includes:
- A SHACL shape (`shape.ttl`)  
- A fill-in JSON-LD template (`content.template.jsonld`)  
- A working example (`content.sample.jsonld`)  
- A CSV header template (`csv-template.csv`)  
- Optional validation reports and guidance

---

## Repository Contents

| Folder | Purpose |
|--------|----------|
| **model/** | Core ontology (`adv-core.ttl`) and IDS validation shapes (`ids-wrapper-shapes.ttl`). |
| **offers/** | IDS offer templates that describe how data is published and discovered. |
| **profiles/** | The five operational profiles with SHACL, JSON-LD, and CSV templates. |
| **aim/** | Integration materials for the Agriculture Information Model (AIM). |
| **validate/** | A ready-to-use validator script (`adv-validate.py`) that checks data files. |
| **registry/** | FAIR-style metadata registry describing each artifact. |
| **w3id/** | Instructions for permanent namespace setup under `https://w3id.org/adv/`. |
| **docs/** | Additional user and developer notes. |

---

## Using the ADV Model

### Step 1 – Choose Your Profile
Select the profile that fits your data (for example, **observation** if you have sensor readings).

### Step 2 – Prepare Your Data
Open the JSON-LD template in the chosen profile folder.  
Replace the placeholder values with your real data.  
You can also fill in the CSV template and convert it to JSON-LD using simple scripts.

### Step 3 – Describe the Dataset
Duplicate `offers/offer.template.jsonld`, fill the metadata fields (`dct:title`, `dct:description`, `adv:profileId`, `adv:profileVersion`, etc.), and link to your dataset’s endpoint or file.

### Step 4 – Validate
Run the included validator to make sure both files conform:

python validate/adv-validate.py --wrapper offers/offer.sample.jsonld --content profiles/observation/content.sample.jsonld

The script:
- Checks the IDS wrapper against `model/ids-wrapper-shapes.ttl`
- Checks the AIM content against the relevant SHACL shape
- Verifies that the declared `adv:profileId` matches the actual AIM class used in the content

### Step 5 – Publish or Exchange
Once validation passes, your data package is **ADV-compliant** and ready to be shared through an IDS connector or any compatible data space environment.

---

## Using AIM (Agriculture Information Model)

ADV profiles reuse AIM classes and properties for meaning.  
You do **not** need to install or copy AIM yourself — all references are stable URLs under `https://w3id.org/aim#`.

To help implementers:

- The folder **`aim/`** contains  
  - `aim-quick-reference.md` – a short guide describing only the AIM terms actually used by ADV.  
  - `pinned-import.ttl` – a small file that imports the official AIM ontology (useful for tools that want a local entry point).

- ADV Data Model v1.1 targets AIM version: **October 2025 release**, namespace root `https://w3id.org/aim#`.

If you need more AIM detail, visit the official AIM repository:  
https://github.com/AgricultureInformationModel/AIM

---

## Validation and Interoperability

Validation is performed with **SHACL** rules to guarantee consistent data structures across pilots.  
This ensures:
- Data discoverability and usability in IDS-based data spaces.  
- Interoperability between applications using the same profiles.  
- Easier extension with local properties without breaking compatibility.

---

## FAIR and Reuse

Each artifact is documented in `registry/artifacts-metadata.json` with:
- version, path, and license  
- last update date  
- file format  

All assets are licensed under **Creative Commons Attribution 4.0 International (CC BY 4.0)**.

---

## Why Only Five Profiles

These profiles were selected to cover 90 % of data types across the AgriDataValue pilots.  
They can be easily extended if new scenarios arise (for example, market data or EO scenes) following the same design pattern.

---

## How to Extend or Contribute

1. Create a new folder under `profiles/` following the same structure.  
2. Add a SHACL shape, JSON-LD template, and sample file.  
3. Register the new profile in `model/adv-core.ttl`.  
4. Validate it with the existing script before submitting.

See `CONTRIBUTING.md` for full contribution guidelines.

---

## License

This project is licensed under **Creative Commons Attribution 4.0 International (CC BY 4.0)**.  
You are free to share and adapt the model as long as proper credit is given.

---

**AgriDataValue Data Model**  
Developed under Horizon Europe Grant Agreement 101086461
