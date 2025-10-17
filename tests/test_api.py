import io
import json
import types
import pytest

from app.api.main import app

@pytest.fixture()
def client():
    app.config.update({"TESTING": True})
    with app.test_client() as client:
        yield client


def test_healthz(client):
    res = client.get('/healthz')
    assert res.status_code == 200
    assert res.get_json()["status"] == "ok"


def test_generate_requires_prompt(client, monkeypatch):
    res = client.post('/generate', json={})
    assert res.status_code == 400


def test_generate_returns_image(client, monkeypatch):
    # Mock the model to avoid heavy dependency & network
    from app import ml as ml_pkg
    # Create a fake image object with save method
    class _FakeImage:
        def save(self, buf, fmt):
            buf.write(b"\x89PNG\r\n\x1a\n")
    fake_module = types.SimpleNamespace(model=types.SimpleNamespace(generate_image=lambda prompt: _FakeImage()))

    monkeypatch.setattr(ml_pkg, 'model', fake_module.model)

    res = client.post('/generate', json={"prompt": "a cat"})
    assert res.status_code == 200
    assert res.mimetype == 'image/png'
    data = res.data
    assert data.startswith(b"\x89PNG")

