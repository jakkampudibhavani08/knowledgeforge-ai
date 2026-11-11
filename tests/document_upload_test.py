
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


def test_valid_pdf_upload(client, tmp_path):
    import fitz

    # Create a real PDF document
    pdf = fitz.open()
    pdf.new_page()
    content = pdf.tobytes()
    pdf.close()

    # Upload the PDF
    response = client.post(
        "/documents/upload",
        files={
            "file": (
                "sample.pdf",
                content,
                "application/pdf"
            )
        }
    )

    # Verify successful upload
    assert response.status_code == 201

    data = response.json()

    # Verify the PDF was saved in the temporary folder
    saved_file = tmp_path / data["new_filename"]

    assert saved_file.exists()
    assert saved_file.read_bytes() == content


def test_duplicate_filenames(client, tmp_path):
    content = b"KnowledgeForge AI test"

    files = {
        "file": (
            "sample.txt",
            content,
            "text/plain"
        )
    }

    # Upload the same filename twice
    response1 = client.post("/documents/upload", files=files)
    response2 = client.post("/documents/upload", files=files)

    # Both uploads must succeed
    assert response1.status_code == 201
    assert response2.status_code == 201

    data1 = response1.json()
    data2 = response2.json()

    # Each upload must have a different UUID
    assert data1["file_id"] != data2["file_id"]

    # Both files must exist separately
    file1 = tmp_path / data1["new_filename"]
    file2 = tmp_path / data2["new_filename"]

    assert file1.exists()
    assert file2.exists()

    assert file1.read_bytes() == content
    assert file2.read_bytes() == content
