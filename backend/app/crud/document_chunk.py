from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.document_chunk import DocumentChunk
from app.services.embedding_service import generate_embeddings


def create_document_chunks(
    db: Session,
    document_id: int,
    chunks: list[str],
) -> list[DocumentChunk]:
    """Create document chunks and store their embedding vectors."""

    if not chunks:
        return []

    embeddings = generate_embeddings(chunks)
    print("NUMBER OF EMBEDDINGS:", len(embeddings))
    print("VECTOR SIZE:", len(embeddings[0]))
    print("EMBEDDING TEST:", type(embeddings))
    print("COUNT:", len(embeddings))
    print("VECTOR SIZE:", len(embeddings[0]))
    document_chunks = [
        DocumentChunk(
            document_id=document_id,
            chunk_index=index,
            content=content,
            embedding=embedding,
        )
        for index, (content, embedding) in enumerate(
            zip(chunks, embeddings, strict=True)
        )
    ]

    db.add_all(document_chunks)
    db.commit()

    for chunk in document_chunks:
        db.refresh(chunk)

    return document_chunks


def get_document_chunks(
    db: Session,
    document_id: int,
) -> list[DocumentChunk]:
    """Return a document's chunks in their original order."""

    stmt = (
        select(DocumentChunk)
        .where(DocumentChunk.document_id == document_id)
        .order_by(DocumentChunk.chunk_index)
    )

    return list(db.execute(stmt).scalars().all())