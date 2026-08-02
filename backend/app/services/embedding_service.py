from sentence_transformers import SentenceTransformer

MODEL_NAME = "all-MiniLM-L6-v2"

_model = SentenceTransformer(MODEL_NAME)


def generate_embedding(text: str) -> list[float]:
    """Generate an embedding vector for a single text string."""
    embedding = _model.encode(text)

    return embedding.tolist()


def generate_embeddings(texts: list[str]) -> list[list[float]]:
    """Generate embedding vectors for multiple text strings."""
    embeddings = _model.encode(texts)

    return embeddings.tolist()