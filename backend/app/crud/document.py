from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.document import Document


def create_document(
    db: Session,
    owner_id: int,
    filename: str,
    original_filename: str,
    file_type: str,
    file_size: int,
) -> Document:
    document = Document(
        owner_id=owner_id,
        filename=filename,
        original_filename=original_filename,
        file_type=file_type,
        file_size=file_size,
    )

    db.add(document)
    db.commit()
    db.refresh(document)

    return document


def get_document(
    db: Session,
    document_id: int,
    owner_id: int,
) -> Document | None:
    stmt = select(Document).where(
        Document.id == document_id,
        Document.owner_id == owner_id,
    )

    return db.execute(stmt).scalar_one_or_none()


def list_documents(
    db: Session,
    owner_id: int,
) -> list[Document]:
    stmt = (
        select(Document)
        .where(Document.owner_id == owner_id)
        .order_by(Document.uploaded_at.desc())
    )

    return list(db.execute(stmt).scalars().all())


def delete_document(
    db: Session,
    document: Document,
) -> None:
    db.delete(document)
    db.commit()