# cowpilot
CoW solver - multi-DEX routing, gas optimization, risk controls

## Generate Pydantic models from OpenAPI

This project can generate Pydantic v2 data models from the OpenAPI file at `app/models/openapi.yml` using `datamodel-code-generator` (dev dependency).

Generate models:

```
poetry install  # ensure dev deps are installed
poetry run generate-schemas
```

This produces `app/schemas_generated.py`. To use the generated models, import from `app.schemas_generated` in your code (or replace imports currently pointing at `app.schemas`).

Notes:
- The generator does not overwrite your hand-written `app/schemas.py`.
- If `datamodel-code-generator` is not installed, the script will print a helpful message.
