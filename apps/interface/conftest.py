"""
Pytest configuration for interface tests
Sets up fixtures for Playwright browser testing
"""

import sys
from pathlib import Path
import pytest
from apps.interface.server import app
import uvicorn
import threading
import time

# Add the project root to Python path so we can import apps
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


@pytest.fixture(scope="session")
def live_server():
    """Start a live server for browser tests"""
    # Start server in a separate thread
    config = uvicorn.Config(
        app,
        host="127.0.0.1",
        port=3001,  # Use a different port to avoid conflicts
        log_level="error",
    )
    server = uvicorn.Server(config)

    thread = threading.Thread(target=server.run, daemon=True)
    thread.start()

    # Wait for server to start
    time.sleep(1)

    yield "http://127.0.0.1:3001"

    # Server will stop when thread dies (daemon=True)


@pytest.fixture(scope="session")
def browser_type_launch_args():
    """Configure browser launch arguments"""
    return {
        "headless": True,  # Run in headless mode for CI/CD
    }


@pytest.fixture(scope="session")
def browser_context_args():
    """Configure browser context"""
    return {
        "viewport": {"width": 1280, "height": 720},
    }
