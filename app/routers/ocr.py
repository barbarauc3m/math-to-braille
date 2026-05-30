from fastapi import APIRouter, HTTPException, UploadFile, File
from pydantic import BaseModel

from app.services.ocr_service import run_ocr, OCRServiceError
from app.utils.validation import validate_mime

router = APIRouter(prefix="/api", tags=["ocr"])


class OCRResponse(BaseModel):
    filename: str
    latex: str


@router.post("/ocr", response_model=OCRResponse)
async def ocr_endpoint(file: UploadFile = File(...)):
    """
    Recibe una imagen, aplica OCR matemático con pix2tex
    y devuelve el LaTeX extraído.
    """
    content = await file.read()

    # Reutilizamos la validación MIME ya implementada
    try:
        validate_mime(content)
    except ValueError as exc:
        raise HTTPException(status_code=415, detail=str(exc))

    try:
        latex = run_ocr(content, file.filename or "imagen")
    except OCRServiceError as exc:
        raise HTTPException(status_code=422, detail=str(exc))

    return OCRResponse(filename=file.filename or "imagen", latex=latex)