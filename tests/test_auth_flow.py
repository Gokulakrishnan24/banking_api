import requests

def test_login(auth_token):
    assert auth_token is not None
    assert len(auth_token) > 10

def test_auth_headers(auth_token):
    x = auth_token
    headers = {"Authorization": f"Bearer {x}"}
    assert "Authorization" in headers
    assert headers["Authorization"].startswith("Bearer ")

def test_fetch_account_details(base_url, auth_token):
    x = auth_token
    headers = {"Authorization": f"Bearer {x}"}
    response = requests.get(f"{base_url}/account/details", headers=headers)
    assert response.status_code == 200

def test_fetch_card_list(base_url, auth_token):
    x = auth_token
    headers = {"Authorization": f"Bearer {x}"}
    response = requests.get(f"{base_url}/cards/list", headers=headers)
    assert response.status_code == 200
