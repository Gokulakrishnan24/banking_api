import requests

CARD_TO_BLOCK = "4111222233334444"  # Matches dummy card in cards.py
INVALID_CARD = "9999-8888-7777-0000"

def test_get_card_list(base_url, auth_token):
    x = auth_token
    headers = {"Authorization": f"Bearer {x}"}
    resp = requests.get(f"{base_url}/cards/list", headers=headers)
    assert resp.status_code == 200
    assert any(card["card_number"] == CARD_TO_BLOCK for card in resp.json())

def test_block_card_success(base_url, auth_token, ensure_card_unblocked):
    x = auth_token
    headers = {"Authorization": f"Bearer {auth_token}"}
    payload = {
        "card_number": CARD_TO_BLOCK,
        "reason": "Suspicious activity"
    }
    resp = requests.post(
        f"{base_url}/cards/block",
        headers=headers,
        json=payload
    )
    assert resp.status_code == 200
    assert "blocked" in resp.json().get("message", "").lower()

def test_block_card_again_should_fail(base_url, auth_token):
    x = auth_token
    headers = {"Authorization": f"Bearer {x}"}
    payload = {
        "card_number": CARD_TO_BLOCK,
        "reason": "Repeated attempt"
    }
    resp = requests.post(
        f"{base_url}/cards/block",
        headers=headers,
        json=payload
    )
    assert resp.status_code == 409
    assert "already blocked" in resp.json().get("detail", "").lower()

def test_block_invalid_card(base_url, auth_token):
    x = auth_token
    headers = {"Authorization": f"Bearer {x}"}
    payload = {
        "card_number": INVALID_CARD,
        "reason": "Invalid test card"
    }
    resp = requests.post(
        f"{base_url}/cards/block",
        headers=headers,
        json=payload
    )
    assert resp.status_code == 404
    assert "not found" in resp.json().get("detail", "").lower()
