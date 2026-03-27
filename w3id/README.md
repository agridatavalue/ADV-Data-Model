# W3ID Setup for ADV Namespaces

We use W3ID permanent IRIs like:
- https://w3id.org/adv/core#

## Option A — GitHub Pages (recommended)
1. Create a public repo `adv-w3id` with directory `adv/`.
2. Add a `_redirects` file (or `.htaccess`) under `adv/` with:
   /core   https://your-org.github.io/adv-data-model/model/adv-core.ttl  302
   /core#  https://your-org.github.io/adv-data-model/model/adv-core.ttl  302
3. Open a PR to https://github.com/perma-id/w3id.org adding `/adv` folder that points to your repo’s `adv/`.

## Option B — Any static host
Serve `adv/core` and `adv/core#` to your ontology TTL and/or docs page via HTTP 301/302.

## Notes
- During development, it’s normal that W3ID URIs don’t resolve in the browser. They are identifiers first.
- When published, keep redirects stable across versions. Include a dated tag if you want versioned docs.
