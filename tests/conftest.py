import pytest
import sys
from pathlib import Path
from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).parent.parent))


@pytest.fixture
def api_client():
    from apps.api.main import app

    return TestClient(app)


@pytest.fixture
def inference_client():
    from apps.inference.server import app

    return TestClient(app)


@pytest.fixture
def interface_client():
    from apps.interface.server import app

    return TestClient(app)
