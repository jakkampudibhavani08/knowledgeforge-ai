from pydantic import BaseModel, Field
from typing import Optional

class DocumentUploadResponse(BaseModel):
    message: str
    file_id: str
    original_filename: str
    new_filename: str
    size: int = Field(ge=1, le=10 * 1024 * 1024)
    file_path: str
    format_type: str

class ExtractedPage(BaseModel):
    Page_number: Optional[int]
    text: str

class DocumentExtractionResponse(BaseModel):
    document_id: str
    filename: str
    pages: list[ExtractedPage]