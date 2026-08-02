from sqlalchemy.orm import Session

from app.models.document_chunk import DocumentChunk


def search_similar_chunks(
    db: Session,
    query_embedding: list[float],
    document_id: int,
    limit: int = 5,
):
    """
    Find similar chunks from a specific document.
    """

    chunks = (
        db.query(DocumentChunk)
        .filter(
            DocumentChunk.document_id == document_id,
            DocumentChunk.embedding.isnot(None),
        )
        .order_by(
            DocumentChunk.embedding.cosine_distance(query_embedding)
        )
        .limit(limit)
        .all()
    )

    return chunks