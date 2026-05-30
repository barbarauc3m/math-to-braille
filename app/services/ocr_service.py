import io
import logging
from functools import lru_cache
from pathlib import Path

from PIL import Image

logger = logging.getLogger(__name__)


@lru_cache(maxsize=1)
def _get_model():
    """
    Carga el modelo una sola vez y lo cachea en memoria.
    La primera ejecución descarga el checkpoint automáticamente.
    """
    from pix2tex.cli import LatexOCR
    logger.info("Cargando modelo pix2tex...")
    model = LatexOCR()
    logger.info("Modelo pix2tex cargado.")
    return model


class OCRServiceError(Exception):
    pass


def run_ocr(file_bytes: bytes, filename: str) -> str:
    """
    Recibe los bytes de una imagen y devuelve el LaTeX extraído.

    Args:
        file_bytes: Contenido binario del archivo.
        filename:   Nombre original (para logs).

    Returns:
        Cadena LaTeX con la fórmula detectada.

    Raises:
        OCRServiceError: Si la imagen no se puede procesar.
    """
    try:
        image = Image.open(io.BytesIO(file_bytes)).convert("RGB")
    except Exception as exc:
        raise OCRServiceError(
            f"No se pudo abrir la imagen '{filename}': {exc}"
        ) from exc

    try:
        model = _get_model()
        latex: str = model(image)
    except Exception as exc:
        raise OCRServiceError(
            f"El modelo pix2tex no pudo procesar '{filename}': {exc}"
        ) from exc

    if not latex or not latex.strip():
        raise OCRServiceError(
            f"pix2tex no detectó ninguna fórmula en '{filename}'."
        )

    logger.info("OCR completado para '%s': %s", filename, latex[:80])
    return latex.strip()