import requests

CARD_TO_BLOCK = "1111-2222-3333-4444"
INVALID_CARD = "9999-8888-7777-0000"

def test_get_card_list(base_url, auth_header):
    resp = requests.get(f"{base_url}/cards/list", headers=auth_header)
    assert resp.status_code == 200
    cards = resp.json().get("cards", [])
    assert any(card["card_number"] == CARD_TO_BLOCK for card in cards)

def test_block_card_success(base_url, auth_header):
    resp = requests.put(
        f"{base_url}/cards/block",
        headers=auth_header,
        json={"card_number": CARD_TO_BLOCK}
    )
    assert resp.status_code == 200
    assert "blocked successfully" in resp.json().get("message", "")

def test_block_card_again_should_fail(base_url, auth_header):
    resp = requests.put(
        f"{base_url}/cards/block",
        headers=auth_header,
        json={"card_number": CARD_TO_BLOCK}
    )
    assert resp.status_code == 409
    assert "already blocked" in resp.json().get("detail", "")

def test_block_invalid_card(base_url, auth_header):
    resp = requests.put(
        f"{base_url}/cards/block",
        headers=auth_header,
        json={"card_number": INVALID_CARD}
    )
    assert resp.status_code == 404
    assert "not found" in resp.json().get("detail", "")
