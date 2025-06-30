import pytest
import requests
import os
from dotenv import load_dotenv

# Load username/password from .env
load_dotenv()

@pytest.fixture(scope="session")
def base_url():
    return "http://localhost:8000"

@pytest.fixture(scope="session")
def credentials():
    return {
        "username": os.getenv("USERNAME", "defaultuser"),
        "password": os.getenv("PASSWORD", "defaultpass")
    }

@pytest.fixture(scope="session")
def auth_token(base_url, credentials):
    """Returns a fresh JWT access token"""
    response = requests.post(f"{base_url}/auth/login", json=credentials)
    assert response.status_code == 200, f"Login failed: {response.text}"
    return response.json()["access_token"]

@pytest.fixture
def auth_header(auth_token):
    """Returns header with Authorization: Bearer <token>"""
    return {"Authorization": f"Bearer {auth_token}"}

import pytest
import requests

CARD_TO_BLOCK = "4111222233334444"

@pytest.fixture
def ensure_card_unblocked(base_url, auth_token):
    """Ensure test card is unblocked before tests."""
    headers = {"Authorization": f"Bearer {auth_token}"}
    resp = requests.post(
        f"{base_url}/cards/unblock",
        headers=headers,
        json={"card_number": CARD_TO_BLOCK}
    )
    # Optional: check/log the message
    return resp

