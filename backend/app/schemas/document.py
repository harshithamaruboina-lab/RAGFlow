from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.models.document import DocumentStatus


class DocumentOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    filename: str
    original_filename: str
    file_type: str
    file_size: int
    status: DocumentStatus
    uploaded_at: datetime
    error_message: str | None = None


class DocumentListResponse(BaseModel):
    total: int
    documents: list[DocumentOut]