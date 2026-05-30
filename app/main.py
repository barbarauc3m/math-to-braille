from fastapi import FastAPI

from app.models import HealthResponse
from app.routers import ocr

app = FastAPI(
    title="mathbraille",
    description="Sistema de traducción de fórmulas matemáticas a Braille",
    version="0.1.0",
)

app.include_router(ocr.router)


@app.get("/health", response_model=HealthResponse)
def health():
    return HealthResponse(status="ok")