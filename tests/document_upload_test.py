
def test_valid_doc_upload(client, tmp_path):
    content = b"KnowledgeForge AI test document"

    response = client.post(
        "/documents/upload",
        files={
            "file": (
                "sample.txt",
                content,
                "text/plain"
            )
        }
    )

    assert response.status_code == 201

    data = response.json()
    assert "file_id" in data

    # Verify file was saved in temporary folder
    saved_file = tmp_path / data["new_filename"]

    assert saved_file.exists()
    assert saved_file.read_bytes() == content


def test_unsupported_file_type(client):
    response = client.post(
        "/documents/upload",
        files={
            "file": (
                "sample.doc",
                b"KnowledgeForge AI test document",
                "text/plain"
            )
        }
    )

    assert response.status_code == 415


def test_doc_size(client):
    oversized_content = b"A" * (10 * 1024 * 1024 + 1)

    response = client.post(
        "/documents/upload",
        files={
            "file": (
                "sample.txt",
                oversized_content,
                "text/plain"
            )
        }
    )

    assert response.status_code == 413


def test_empty_file(client):
    response = client.post(
        "/documents/upload",
        files={
            "file": (
                "sample.txt",
                b"",
                "text/plain"
            )
        }
    )

    assert response.status_code == 400


def test_fake_pdf_upload(client):
    response = client.post(
        "/documents/upload",
        files={
            "file": (
                "fake.pdf",
                b"Hello, I am actually a text file!",
                "application/pdf"
            )
        }
    )

    assert response.status_code == 400


def test_invalid_txt_upload(client):
    response = client.post(
        "/documents/upload",
        files={
            "file": (
                "invalid.txt",
                b"\xff\xfe\x00\x80",
                "text/plain"
            )
        }
    )

    assert response.status_code == 400
