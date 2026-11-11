from fastapi.testclient import TestClient 
from app.main import app 

client=TestClient(app)

def test_valid_doc_upload():
    response=client.post("/documents/upload",
                         files={"file":("sample.txt",b"KnowledgeForge AI test document","text/plain")})
    assert response.status_code==201 
    assert "file_id" in response.json() 

def test_unsupported_file_type():
    response=client.post("/documents/upload",
                             files={"file":("sample.doc",b"KnowledgeForge AI test document","text/plain")})
    assert response.status_code==415 

def test_doc_size():
    oversized_len=b"A"*(10*1024*1024+1)
    response=client.post("/documents/upload",
                             files={"file":("sample.txt",oversized_len,"text/plain")})
    assert response.status_code==413

def test_empty_file():
    response=client.post("/documents/upload",
                                 files={"file":("sample.txt",b"","text/plain")})

    assert response.status_code==400 


def test_fake_pdf_upload():
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


def test_invalid_txt_upload():
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






