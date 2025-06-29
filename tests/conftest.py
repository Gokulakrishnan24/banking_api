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
