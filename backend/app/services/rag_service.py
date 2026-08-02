from sqlalchemy.orm import Session

from app.services.embedding_service import generate_embedding
from app.services.retrieval_service import search_similar_chunks
from app.services.llm_service import generate_answer


def ask_question(
    db: Session,
    question: str,
    document_id: int,
):

    # 1. Create query embedding
    query_embedding = generate_embedding(question)


    # 2. Retrieve chunks
    chunks = search_similar_chunks(
        db,
        query_embedding,
        document_id=document_id,
        limit=5,
    )


    # 3. Build context
    context = "\n\n".join(
        chunk.content
        for chunk in chunks
    )


    print("====== RETRIEVED CONTEXT ======")
    print(context)
    print("====== END CONTEXT ======")



    # 4. Prompt
    prompt = f"""
You are a helpful assistant answering questions about a document.

Use ONLY the provided context.

If the answer exists in the context, answer clearly.

Context:

{context}


Question:

{question}


Answer:
"""


    # 5. Generate answer
    answer = generate_answer(prompt)



    print("====== OLLAMA ANSWER ======")
    print(answer)
    print("============================")



    # 6. Prepare sources
    sources = []

    for chunk in chunks:
        sources.append(
            {
                "chunk_id": chunk.id,
                "document_id": chunk.document_id,
                "chunk_index": chunk.chunk_index,
                "content": chunk.content,
            }
        )


    return {
        "answer": answer,
        "sources": sources,
    }