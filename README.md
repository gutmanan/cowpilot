# Cowpilot
CoW solver - multi-DEX routing, gas optimization, risk controls

## Generate Pydantic models from OpenAPI

Currently we do not maintain a generation script. 
To (re)generate the Pydantic v2 data models from the OpenAPI spec, run `datamodel-codegen` directly against `resources/openapi.yml`:

```
poetry install  # ensure dev deps are installed (includes datamodel-code-generator)
poetry run datamodel-codegen \
  --input resources/openapi.yml \
  --input-file-type openapi \
  --output app/schemas_generated.py \
  --target-python-version 3.10 \
  --output-model-type pydantic_v2.BaseModel \
  --use-standard-collections \
  --use-schema-description \
  --disable-timestamp \
  --wrap-string-literal \
  --snake-case-field \
  --enum-field-as-literal one
```

This produces `app/schemas_generated.py`. Import generated models from `app.schemas_generated`.

## Run the server (dev)

Use uvicorn via poetry:

```
poetry run uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```
