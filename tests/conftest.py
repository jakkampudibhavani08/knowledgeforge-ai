
import pytest
from pathlib import Path
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture
def client(tmp_path):

    # the original folders
    original_upload_dir = app.state.upload_dir
    original_extracted_dir = app.state.extracted_dir

    # Create temporary paths for testing
    app.state.upload_dir = tmp_path
    app.state.extracted_dir = tmp_path / "extracted"

    # Create temporary uploads directory
    app.state.upload_dir.mkdir(parents=True, exist_ok=True)

    try:
        with TestClient(app) as test_client:
            yield test_client

    finally:
        # Restore original paths
        app.state.upload_dir = original_upload_dir
        app.state.extracted_dir = original_extracted_dir
