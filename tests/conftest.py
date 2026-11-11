
import pytest
from pathlib import Path
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture
def client(tmp_path):

    # Remember the normal uploads folder
    original_upload_dir = getattr(
        app.state,
        "upload_dir",
        Path("uploads")
    )

    # Use temporary storage during this test
    app.state.upload_dir = tmp_path

    try:
        with TestClient(app) as test_client:
            yield test_client

    finally:
        # Restore normal storage after the test
        app.state.upload_dir = original_upload_dir
