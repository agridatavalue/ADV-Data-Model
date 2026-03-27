# Contributing to the AgriDataValue (ADV) Data Model

Thank you for your interest in contributing!  
The ADV Data Model is a shared effort across the AgriDataValue consortium to ensure **semantic interoperability** and **ease of use** for all pilot implementations.

---

## 🧭 Guiding Principles
1. **Clarity over complexity** — Everything should be understandable by users without ontology expertise.  
2. **Practical interoperability** — Focus on the data actually exchanged in pilots.  
3. **Minimalism first** — Add only what’s needed; simplify before expanding.  
4. **Backward compatibility** — Existing profiles should continue to work as new ones are introduced.  
5. **FAIR compliance** — All artifacts must remain *Findable, Accessible, Interoperable, and Reusable.*

---

## 🧩 How to Contribute

### 1. Reporting Issues or Suggestions
- Use the **GitHub Issues** tab to report bugs, request new features, or suggest clarifications.
- When describing a change, clearly state the:
  - Affected profile or file (e.g., `profiles/observation/shape.ttl`)
  - Expected vs actual behavior
  - Example data (if applicable)

### 2. Proposing Edits
To propose a change or addition:
1. Fork the repository.  
2. Create a feature branch:  
   `git checkout -b feature/my-improvement`  
3. Make your edits:
   - RDF/Turtle files → keep consistent prefixes and indentation.  
   - JSON-LD templates → validate JSON syntax.  
   - SHACL shapes → verify with `validate/adv-validate.py` before committing.  
4. Commit and push your branch.  
5. Submit a **Pull Request** with a clear summary of your change.

### 3. Validation Before Commit
All modified or new profiles **must** pass SHACL validation:

python validate/adv-validate.py --wrapper offers/offer.sample.jsonld --content profiles/<your-profile>/content.sample.jsonld

If you introduce a new profile:
- Add its declaration to `model/adv-core.ttl`.  
- Create corresponding `shape.ttl`, `content.template.jsonld`, and `content.sample.jsonld` files.  
- Update the README table of profiles.

---

## 🧪 Adding New Profiles
When adding a new profile:
1. Follow the naming pattern `adv.<profileName>` (e.g., `adv.market`).  
2. Place it under `profiles/<profileName>/`.  
3. Include:  
   - `shape.ttl` (constraints)  
   - `content.template.jsonld` (editable template)  
   - `content.sample.jsonld` (example)  
   - Optional `csv-template.csv`  
4. Reference it in:  
   - `model/adv-core.ttl`  
   - README profile table  

---

## 🧰 Development Recommendations
- Use **RDF 1.1 Turtle syntax** (`.ttl`) with standard prefixes (`rdfs:`, `dct:`, `xsd:`).  
- Run `rdflib` or an RDF validator to check syntax.  
- Follow semantic versioning:  
  - **MAJOR** — breaking changes  
  - **MINOR** — backward-compatible additions  
  - **PATCH** — corrections or clarifications  

---

## 🧑‍🤝‍🧑 Governance
- Changes are reviewed by the **AgriDataValue consortium**.  
- Major changes are discussed and approved jointly with WP1 and WP3 leads.  

---

## 🪪 License
By contributing, you agree that your contributions will be licensed under the **Creative Commons Attribution 4.0 International (CC BY 4.0)** license.

---

**AgriDataValue Data Model**  
Developed under Horizon Europe Grant Agreement 101086461
