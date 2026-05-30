from pydantic import BaseModel


class HealthResponse(BaseModel):
    status: str


class OCRResponse(BaseModel):
    filename: str
    latex: str