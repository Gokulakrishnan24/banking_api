import requests


NEW_EMAIL = "updated.email@example.com"
NEW_PHONE = "9876543210"

def test_contact_update_flow(base_url, auth_header):
    # Step 1: Fetch before update
    response = requests.get(f"{base_url}/account/details", headers=auth_header)
    assert response.status_code == 200

    # Step 2: Update
    payload = {"email": NEW_EMAIL, "phone": NEW_PHONE}
    update = requests.put(f"{base_url}/update-contact", headers=auth_header, json=payload)
    assert update.status_code == 200

    # Step 3: Fetch after update
    updated = requests.get(f"{base_url}/account/details", headers=auth_header).json()
    assert updated["email"] == NEW_EMAIL
    assert updated["phone"] == NEW_PHONE

