# Text-to-Image App

Simple web app that converts text prompts to images using Stable Diffusion (via Hugging Face diffusers). Includes API, UI, Dockerfile, tests, and CI.

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export FLASK_APP=app.api.main:app
flask run --host 0.0.0.0 --port 8000
```

Open http://localhost:8000

## API

- `GET /healthz` → `{ "status": "ok" }`
- `POST /generate` body: `{ "prompt": "a cat" }` → returns PNG image

## Run tests

```bash
pytest -q
```

## Docker

Build and run:

```bash
docker build -t text2img .
docker run --rm -p 8000:8000 text2img
```

## CI/CD

GitHub Actions workflow runs tests and builds the image on each push.