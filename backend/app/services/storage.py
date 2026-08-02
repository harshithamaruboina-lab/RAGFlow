import uuid
from pathlib import Path

from fastapi import UploadFile

from app.core.config import settings
from app.core.exceptions import AppError

CHUNK_SIZE = 1024 * 1024  # 1 MB, streamed to avoid loading whole file into memory


def get_file_extension(filename: str) -> str:
    return Path(filename).suffix.lower().lstrip(".")


def validate_extension(filename: str) -> str:
    extension = get_file_extension(filename)
    if not extension:
        raise AppError("Uploaded file must have a valid extension.", status_code=400)
    if extension not in settings.allowed_file_types_list:
        allowed = ", ".join(settings.allowed_file_types_list)
        raise AppError(
            f"File type '.{extension}' is not supported. Allowed types: {allowed}.",
            status_code=415,
        )
    return extension


def generate_stored_filename(extension: str) -> str:
    # Random UUID filename — the original filename is never used on disk,
    # which is what prevents path traversal / collision / overwrite attacks.
    return f"{uuid.uuid4().hex}.{extension}"


def resolve_safe_path(stored_filename: str) -> Path:
    upload_dir = settings.upload_dir_path.resolve()
    target_path = (upload_dir / stored_filename).resolve()
    if target_path != upload_dir and upload_dir not in target_path.parents:
        raise AppError("Invalid file path.", status_code=400)
    return target_path


async def save_upload_file(upload_file: UploadFile) -> tuple[str, str, int]:
    """
    Validates and streams an uploaded file to disk.

    Returns (stored_filename, extension, file_size_bytes).
    Raises AppError on validation failure and cleans up any partial write.
    """
    original_filename = upload_file.filename or ""
    extension = validate_extension(original_filename)
    stored_filename = generate_stored_filename(extension)
    destination = resolve_safe_path(stored_filename)

    max_bytes = settings.max_upload_size_bytes
    total_bytes = 0

    try:
        with destination.open("wb") as buffer:
            while True:
                chunk = await upload_file.read(CHUNK_SIZE)
                if not chunk:
                    break
                total_bytes += len(chunk)
                if total_bytes > max_bytes:
                    raise AppError(
                        f"File exceeds maximum allowed size of {settings.MAX_UPLOAD_SIZE_MB} MB.",
                        status_code=413,
                    )
                buffer.write(chunk)
    except AppError:
        destination.unlink(missing_ok=True)
        raise
    except Exception as exc:
        destination.unlink(missing_ok=True)
        raise AppError(f"Failed to save uploaded file: {exc}", status_code=500) from exc
    finally:
        await upload_file.close()

    if total_bytes == 0:
        destination.unlink(missing_ok=True)
        raise AppError("Uploaded file is empty.", status_code=400)

    return stored_filename, extension, total_bytes


def delete_file_from_disk(stored_filename: str) -> None:
    try:
        path = resolve_safe_path(stored_filename)
        path.unlink(missing_ok=True)
    except AppError:
        pass