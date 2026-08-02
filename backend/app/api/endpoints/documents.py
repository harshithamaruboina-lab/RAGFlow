from app.crud.document_chunk import create_document_chunks

from pathlib import Path

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.orm import Session


from app.core.exceptions import AppError

from app.crud.document import (
    create_document,
    delete_document,
    get_document,
    list_documents,
)

from app.db.session import get_db

from app.schemas.document import (
    DocumentListResponse,
    DocumentOut,
)

from app.services.document_parser import extract_text
from app.services.storage import (
    delete_file_from_disk,
    save_upload_file,
)

from app.services.text_chunker import chunk_text


router = APIRouter()



# =========================
# UPLOAD DOCUMENT
# =========================

@router.post(
    "/upload",
    response_model=DocumentOut,
    status_code=status.HTTP_201_CREATED,
)
async def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="No filename provided",
        )


    try:
        stored_filename, extension, file_size = await save_upload_file(file)

    except AppError as exc:
        raise HTTPException(
            status_code=exc.status_code,
            detail=exc.message,
        )


    # temporary single user
    owner_id = 1


    document = create_document(
        db,
        owner_id=owner_id,
        filename=stored_filename,
        original_filename=file.filename,
        file_type=extension,
        file_size=file_size,
    )


    if extension in {"txt", "pdf", "docx"}:

        try:

            file_path = Path(
                "data/uploads"
            ) / stored_filename


            extracted_text = extract_text(
                file_path
            )


            chunks = chunk_text(
                extracted_text,
                chunk_size=500,
                overlap=50,
            )


            create_document_chunks(
                db,
                document_id=document.id,
                chunks=chunks,
            )


            print(
                f"Processed {file.filename}"
            )


        except Exception as exc:

            print(
                "Document processing failed:",
                exc
            )


    return document





# =========================
# LIST DOCUMENTS
# =========================

@router.get(
    "/",
    response_model=DocumentListResponse,
)
def get_documents(
    db: Session = Depends(get_db),
):

    documents = list_documents(
        db,
        owner_id=1
    )


    return DocumentListResponse(
        total=len(documents),
        documents=documents,
    )





# =========================
# GET SINGLE DOCUMENT
# =========================

@router.get(
    "/{document_id}",
    response_model=DocumentOut,
)
def get_document_by_id(
    document_id:int,
    db:Session = Depends(get_db),
):

    document = get_document(
        db,
        document_id,
        1
    )


    if document is None:

        raise HTTPException(
            status_code=404,
            detail="Document not found",
        )


    return document





# =========================
# DELETE DOCUMENT
# =========================

@router.delete(
    "/{document_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def remove_document(
    document_id:int,
    db:Session = Depends(get_db),
):

    document = get_document(
        db,
        document_id,
        1
    )


    if document is None:

        raise HTTPException(
            status_code=404,
            detail="Document not found",
        )


    delete_file_from_disk(
        document.filename
    )


    delete_document(
        db,
        document
    )


    return None