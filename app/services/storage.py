
import json
from pathlib import Path

from app.schemas import DocumentExtractionResponse


def save_extraction_result(
    result: DocumentExtractionResponse,
    output_dir: Path
):
    output_dir.mkdir(parents=True, exist_ok=True)

    file_path = output_dir / f"{result.document_id}.json"

    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(
            result.model_dump(),
            file,
            ensure_ascii=False,
            indent=2
        )

    return file_path
