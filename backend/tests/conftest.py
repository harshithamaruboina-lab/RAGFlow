import shutil
from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.config import settings
from app.db.base import Base
from app.db.session import get_db
from app.main import app

TEST_DATABASE_URL = "sqlite:///:memory:"


@pytest.fixture()
def db_session_factory():
    engine = create_engine(
        TEST_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    testing_session_local = sessionmaker(bind=engine, autocommit=False, autoflush=False, future=True)
    yield testing_session_local
    Base.metadata.drop_all(bind=engine)
    engine.dispose()


@pytest.fixture()
def client(db_session_factory, tmp_path, monkeypatch) -> Generator[TestClient, None, None]:
    upload_dir = tmp_path / "uploads"
    upload_dir.mkdir()
    monkeypatch.setattr(settings, "UPLOAD_DIR", str(upload_dir))

    def override_get_db():
        db = db_session_factory()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()
    shutil.rmtree(upload_dir, ignore_errors=True)


@pytest.fixture()
def register_and_login(client):
    def _register_and_login(email: str = "user@example.com", password: str = "StrongPass123!"):
        resp = client.post("/api/v1/auth/register", json={"email": email, "password": password})
        assert resp.status_code == 201, resp.text

        login_resp = client.post(
            "/api/v1/auth/login",
            data={"username": email, "password": password},
        )
        assert login_resp.status_code == 200, login_resp.text
        token = login_resp.json()["access_token"]
        return {"Authorization": f"Bearer {token}"}

    return _register_and_login