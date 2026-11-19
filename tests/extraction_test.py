import pymupdf
import pytest
from app.services.extraction import extract_txt, extract_pdf

def test_extract_txt(tmp_path):
    file_path = tmp_path / "sample.txt"
    file_path.write_text("Hello Python", encoding="utf-8")
    result = extract_txt(file_path)
    assert result[0]["Page_number"] is None
    assert result[0]["text"] == "Hello Python"

def test_extract_pdf(tmp_path):
    file_path = tmp_path / "sample.pdf"
    doc = pymupdf.open()
    page = doc.new_page()
    page.insert_text((72, 72), "Hello Python")
    doc.save(file_path)
    doc.close()
    result = extract_pdf(file_path)
    assert result[0]["text"].strip() == "Hello Python"

def test_empty_txt(tmp_path):
    file_path = tmp_path / "empty.txt"
    file_path.write_text("   ", encoding="utf-8")
    with pytest.raises(ValueError, match="No extractable text"):
        extract_txt(file_path)

def test_empty_pdf(tmp_path):
    file_path = tmp_path / "empty.pdf"
    doc = pymupdf.open()
    doc.new_page()
    doc.save(file_path)
    doc.close()
    with pytest.raises(ValueError, match="No extractable text"):
        extract_pdf(file_path)

def test_corrupted_pdf(tmp_path):
    file_path = tmp_path / "corrupted.pdf"
    file_path.write_bytes(b"This is not a real PDF")
    with pytest.raises(Exception):
        extract_pdf(file_path)

def test_invalid_txt_encoding(tmp_path):
    file_path = tmp_path / "invalid.txt"
    file_path.write_bytes(b"\xff\xfe\x80")
    with pytest.raises(UnicodeDecodeError):
        extract_txt(file_path)