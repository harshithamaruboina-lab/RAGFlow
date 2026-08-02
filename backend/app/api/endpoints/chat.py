from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services.rag_service import ask_question


router = APIRouter(
    prefix="/chat",
    tags=["chat"],
)



@router.post("/ask")
def chat(
    question: str,
    document_id: int,
    db: Session = Depends(get_db),
):

    result = ask_question(
        db,
        question,
        document_id,
    )


    return {
        "question": question,
        "document_id": document_id,
        "answer": result["answer"],
        "sources": result["sources"],
    }