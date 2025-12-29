"""
Tests for the interface web server
Tests the FastAPI routes and static file serving
"""

import sys
from pathlib import Path

# Add the project root to Python path so we can import apps
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# Imports after path setup (needed for apps module)
from fastapi.testclient import TestClient  # noqa: E402
from apps.interface.server import app  # noqa: E402
import tempfile  # noqa: E402
import os  # noqa: E402


# Create a test client
client = TestClient(app)

# Paths to test files
INTERFACE_DIR = Path(__file__).parent
STATIC_DIR = INTERFACE_DIR / "static"
TEMPLATES_DIR = INTERFACE_DIR / "templates"


def test_root_route():
    """Test that the root route returns the index.html page"""
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    # Check that it contains some expected HTML content
    assert b"InstruSense" in response.content or b"html" in response.content.lower()


def test_health_route():
    """Test that the health endpoint returns the correct status"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["service"] == "interface"


def test_static_css_file():
    """Test that CSS files are served correctly"""
    response = client.get("/static/css/style.css")
    assert response.status_code == 200
    assert (
        "text/css" in response.headers["content-type"]
        or "text/plain" in response.headers["content-type"]
    )


def test_static_js_file():
    """Test that JavaScript files are served correctly"""
    # Test app.js
    response = client.get("/static/js/app.js")
    assert response.status_code == 200
    content_type = response.headers["content-type"].lower()
    assert "javascript" in content_type or "text/plain" in content_type

    # Test instruments.js
    response = client.get("/static/js/instruments.js")
    assert response.status_code == 200


def test_static_image_file():
    """Test that image files are served correctly"""
    # Test if at least one image exists and can be served
    image_files = list(STATIC_DIR.glob("images/*.jpg"))
    if image_files:
        image_name = image_files[0].name
        response = client.get(f"/static/images/{image_name}")
        assert response.status_code == 200
        assert "image" in response.headers["content-type"].lower()


#  Playwright UI tests


def test_page_loads_and_form_visible(page, live_server):
    page.goto(f"{live_server}/")

    assert page.locator("#uploadForm").is_visible()
    assert page.locator("#audioFile").is_visible()
    assert page.locator("#submitBtn").is_visible()

    # hidden by default
    assert not page.locator("#errorSection").is_visible()
    assert not page.locator("#loadingSection").is_visible()


def test_submit_without_file_shows_error(page, live_server):
    page.goto(f"{live_server}/")

    # Remove the 'required' attribute to allow form submission without file
    # This simulates the case where validation might be bypassed
    page.evaluate("document.getElementById('audioFile').removeAttribute('required')")

    page.locator("#submitBtn").click()

    # wait until error becomes visible
    page.wait_for_selector("#errorSection", state="visible", timeout=2000)

    msg = page.locator("#errorMessage").text_content().lower()
    assert "select" in msg or "file" in msg or "error" in msg


def test_submit_with_file_shows_loader(page, live_server):
    page.goto(f"{live_server}/")

    # create a small dummy file
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
        f.write(b"RIFF....WAVE")  # minimal bytes to look like wav
        temp_file = f.name

    try:
        page.locator("#audioFile").set_input_files(temp_file)
        page.locator("#submitBtn").click()

        page.wait_for_selector("#loadingSection", state="visible", timeout=2000)
        assert page.locator("#loadingSection").is_visible()
    finally:
        if os.path.exists(temp_file):
            os.unlink(temp_file)


def test_modal_open_and_close(page, live_server):
    page.goto(f"{live_server}/")

    page.evaluate(
        """
      const modal = document.getElementById('instrumentModal');
      const img = document.getElementById('modalImage');
      const name = document.getElementById('modalName');

      img.src = '/static/images/records.jpg';
      name.textContent = 'Piano';

      modal.style.display = 'flex';
      modal.classList.add('show');
    """
    )

    page.wait_for_selector("#instrumentModal", state="visible", timeout=2000)
    assert page.locator("#modalName").text_content() == "Piano"

    # close with X
    page.locator("#modalClose").click()
    page.wait_for_selector("#instrumentModal", state="hidden", timeout=2000)
