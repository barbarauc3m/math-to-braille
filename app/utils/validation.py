import magic

from app.config import ALLOWED_MIME_TYPES, MAX_FILE_SIZE_BYTES


def validate_mime(content: bytes) -> str:
    """
    Comprueba el MIME real del contenido (no el que declara el cliente).
    Devuelve el MIME detectado, o lanza ValueError si no está permitido.
    """
    if len(content) > MAX_FILE_SIZE_BYTES:
        raise ValueError(
            f"El archivo supera el límite de {MAX_FILE_SIZE_BYTES // (1024*1024)} MB."
        )

    detected = magic.from_buffer(content, mime=True)

    if detected not in ALLOWED_MIME_TYPES:
        raise ValueError(
            f"Tipo de archivo no permitido: '{detected}'. "
            f"Se aceptan: {', '.join(sorted(ALLOWED_MIME_TYPES))}."
        )

    return detected