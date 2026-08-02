import io


def test_upload_requires_authentication(client):
    files = {"file": ("test.pdf", io.BytesIO(b"%PDF-1.4 fake pdf content"), "application/pdf")}
    response = client.post("/api/v1/documents/upload", files=files)
    assert response.status_code == 401


def test_authenticated_upload_success(client, register_and_login):
    headers = register_and_login()
    files = {"file": ("report.pdf", io.BytesIO(b"%PDF-1.4 fake pdf content"), "application/pdf")}
    response = client.post("/api/v1/documents/upload", files=files, headers=headers)
    assert response.status_code == 201
    body = response.json()
    assert body["original_filename"] == "report.pdf"
    assert body["file_type"] == "pdf"
    assert body["status"] == "uploaded"
    assert body["file_size"] > 0


def test_unsupported_file_type_rejected(client, register_and_login):
    headers = register_and_login()
    files = {"file": ("malware.exe", io.BytesIO(b"fake binary content"), "application/octet-stream")}
    response = client.post("/api/v1/documents/upload", files=files, headers=headers)
    assert response.status_code == 415


def test_document_list_isolated_between_users(client, register_and_login):
    headers_a = register_and_login(email="usera@example.com")
    headers_b = register_and_login(email="userb@example.com")

    files = {"file": ("a_doc.pdf", io.BytesIO(b"%PDF-1.4 content a"), "application/pdf")}
    client.post("/api/v1/documents/upload", files=files, headers=headers_a)

    list_a = client.get("/api/v1/documents/", headers=headers_a)
    list_b = client.get("/api/v1/documents/", headers=headers_b)

    assert list_a.status_code == 200
    assert list_b.status_code == 200
    assert list_a.json()["total"] == 1
    assert list_b.json()["total"] == 0


def test_user_cannot_access_other_users_document(client, register_and_login):
    headers_a = register_and_login(email="ownera@example.com")
    headers_b = register_and_login(email="ownerb@example.com")

    files = {"file": ("private.pdf", io.BytesIO(b"%PDF-1.4 private content"), "application/pdf")}
    upload_resp = client.post("/api/v1/documents/upload", files=files, headers=headers_a)
    document_id = upload_resp.json()["id"]

    response = client.get(f"/api/v1/documents/{document_id}", headers=headers_b)
    assert response.status_code == 404


def test_get_own_document(client, register_and_login):
    headers = register_and_login()
    files = {"file": ("mydoc.pdf", io.BytesIO(b"%PDF-1.4 content"), "application/pdf")}
    upload_resp = client.post("/api/v1/documents/upload", files=files, headers=headers)
    document_id = upload_resp.json()["id"]

    response = client.get(f"/api/v1/documents/{document_id}", headers=headers)
    assert response.status_code == 200
    assert response.json()["id"] == document_id


def test_delete_document(client, register_and_login):
    headers = register_and_login()
    files = {"file": ("todelete.pdf", io.BytesIO(b"%PDF-1.4 content"), "application/pdf")}
    upload_resp = client.post("/api/v1/documents/upload", files=files, headers=headers)
    document_id = upload_resp.json()["id"]

    delete_resp = client.delete(f"/api/v1/documents/{document_id}", headers=headers)
    assert delete_resp.status_code == 204

    get_resp = client.get(f"/api/v1/documents/{document_id}", headers=headers)
    assert get_resp.status_code == 404