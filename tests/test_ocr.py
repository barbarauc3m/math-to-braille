from unittest.mock import patch, MagicMock
from io import BytesIO

import pytest
from fastapi.testclient import TestClient
from PIL import Image

from app.main import app

client = TestClient(app)


def _make_png_bytes() -> bytes:
    """Crea una imagen PNG mínima en memoria."""
    img = Image.new("RGB", (100, 50), color="white")
    buf = BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


@patch("app.services.ocr_service._get_model")
def test_ocr_ok(mock_get_model):
    """El endpoint devuelve LaTeX cuando el modelo responde correctamente."""
    mock_model = MagicMock(return_value=r"\frac{-b \pm \sqrt{b^2-4ac}}{2a}")
    mock_get_model.return_value = mock_model

    response = client.post(
        "/api/ocr",
        files={"file": ("formula.png", _make_png_bytes(), "image/png")},
    )
    assert response.status_code == 200
    data = response.json()
    assert "latex" in data
    assert r"\frac" in data["latex"]


@patch("app.services.ocr_service._get_model")
def test_ocr_empty_result(mock_get_model):
    """Si el modelo devuelve cadena vacía, el endpoint responde 422."""
    mock_model = MagicMock(return_value="")
    mock_get_model.return_value = mock_model

    response = client.post(
        "/api/ocr",
        files={"file": ("formula.png", _make_png_bytes(), "image/png")},
    )
    assert response.status_code == 422


@patch("app.services.ocr_service._get_model")
def test_ocr_model_exception(mock_get_model):
    """Si el modelo lanza excepción, el endpoint responde 422."""
    mock_model = MagicMock(side_effect=RuntimeError("CUDA out of memory"))
    mock_get_model.return_value = mock_model

    response = client.post(
        "/api/ocr",
        files={"file": ("formula.png", _make_png_bytes(), "image/png")},
    )
    assert response.status_code == 422


def test_ocr_invalid_mime():
    """Archivos con MIME inválido son rechazados con 415."""
    response = client.post(
        "/api/ocr",
        files={"file": ("malware.exe", b"MZ\x90\x00fake", "application/octet-stream")},
    )
    assert response.status_code == 415