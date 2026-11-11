from pydantic import BaseModel, Field


class DocumentUploadResponse(BaseModel):
    message: str
    file_id: str
    original_filename: str
    new_filename: str
    size: int = Field(ge=1, le=10 * 1024 * 1024)
    file_path: str
    format_type: str