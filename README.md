# faithful

See all [Cowerx open source tools](https://cowerx.dev/open-source/).

Check whether every number, capitalized name, and product-like identifier in a short model summary appears literally in the source text. This is the deterministic gate used for [Cowerx Daily](https://cowerx.dev/daily/). A pass means the checked tokens occur in the source; it does not prove that the summary's claims are true.

Install: `python3 -m pip install .` from this folder. Run: `faithful source.txt summary.json` (or `python3 -m faithful source.txt summary.json`). The JSON needs `summary` (exactly two sentences) and `why_builder_cares` (one line).

Example `summary.json`:

```json
{"summary":"Alpha has 12 models. Alpha runs locally.","why_builder_cares":"Builders can test Alpha."}
```

With `source.txt` containing `Alpha has 12 models and runs locally. Builders can test Alpha.`, output is:

```text
PASS: all checked tokens appear in source
```

A mismatch prints `FAIL: absent from fetched text: ...` and exits 1. Library: `from faithful import faithful`; pass the JSON object and source string. It returns an empty string on pass, otherwise a reason. Run standalone tests with `python3 -m unittest discover -s tests -v`.
