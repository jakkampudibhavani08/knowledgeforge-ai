import json
from app.schemas import DocumentExtractionResponse
from app.services.storage import save_extraction_result


def test_save_extraction_result(tmp_path):

    result = DocumentExtractionResponse(
        document_id="abc-123",
        filename="sample.pdf",
        pages=[
            {
                "Page_number": 1,
                "text": "Hello KnowledgeForge AI"
            }
        ]
    )

    saved_path = save_extraction_result(result, tmp_path)

    assert saved_path.exists()

    with open(saved_path, "r", encoding="utf-8") as file:
        saved_data = json.load(file)

    assert saved_data["document_id"] == "abc-123"
    assert saved_data["filename"] == "sample.pdf"
    assert saved_data["pages"][0]["text"] == "Hello KnowledgeForge AI"