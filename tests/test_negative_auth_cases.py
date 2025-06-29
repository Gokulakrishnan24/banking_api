import pytest
import requests

@pytest.fixture(scope="session")
def base_url():
    return "http://localhost:8000"  # Replace with env or fixture if using

# ----------------------------
# NEGATIVE TEST: Empty Login
# ----------------------------
def test_login_with_empty_credentials(base_url):
    payload = {
        "username": "",
        "password": ""
    }
    response = requests.post(f"{base_url}/auth/login", json=payload)
    assert response.status_code == 422 or response.status_code == 401
    print("✅ Login failed with empty credentials as expected.")

# ----------------------------
# ✅ Define all secured endpoints that require token
protected_endpoints = [
    ("GET", "/account/details"),
    ("GET", "/cards/list"),
      # Optional
]

@pytest.mark.parametrize("method, endpoint", protected_endpoints)
def test_protected_endpoints_with_empty_token(base_url, method, endpoint):
    url = f"{base_url}{endpoint}"
    headers = {"Authorization": ""}  # Empty token

    # Send the request based on HTTP method
    if method == "GET":
        response = requests.get(url, headers=headers)
    elif method == "POST":
        response = requests.post(url, headers=headers)
    elif method == "PUT":
        response = requests.put(url, headers=headers)
    elif method == "DELETE":
        response = requests.delete(url, headers=headers)
    else:
        pytest.fail(f"Unsupported HTTP method: {method}")

    # Accept 401 or 403 based on FastAPI + APIKeyHeader behavior
    assert response.status_code in (401, 403), f"{method} {endpoint} should return 401 or 403"
    print(f"✅ {method} {endpoint} correctly blocked without token ({response.status_code})")
