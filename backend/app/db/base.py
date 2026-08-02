# Imported by Alembic's env.py so that Base.metadata is aware of every model.
# Every new model module must be imported here.
from app.db.base_class import Base  # noqa: F401
from app.models.user import User  # noqa: F401
from app.models.document import Document  # noqa: F401
from app.models.document_chunk import DocumentChunk  # noqa: F401