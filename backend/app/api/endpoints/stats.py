from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.document import Document
from app.models.document_chunk import DocumentChunk


router = APIRouter(
    prefix="/stats",
    tags=["stats"]
)


@router.get("/")
def get_stats(
    db: Session = Depends(get_db)
):

    documents = db.query(Document).count()

    chunks = db.query(DocumentChunk).count()


    return {

        "documents": documents,

        "chunks": chunks,

        "status": "Online"

    }