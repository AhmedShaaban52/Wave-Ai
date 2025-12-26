import requests

BASE_URL = "http://localhost:3000/api"
TOKEN = "l6OHQemPNaMJBCD04DTGyVuF4r4Rvy2m.JSbslKu4FiAV6LT7o2LW7yS%2FBbkTt8q3Lo8UFKaR6QE%3D"
HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}
TIMEOUT = 30

def test_get_note_by_id_with_authentication():
    note_data = {
        "title": "Test Note for GET",
        "content": "This is a test note to verify GET /note/:id with authentication."
    }

    note_id = None

    # Create note to get valid ID
    try:
        create_resp = requests.post(
            f"{BASE_URL}/note/create",
            json=note_data,
            headers=HEADERS,
            timeout=TIMEOUT
        )
        assert create_resp.status_code == 201 or create_resp.status_code == 200, f"Unexpected status creating note: {create_resp.status_code}"
        created_note = create_resp.json()
        assert "id" in created_note, "Created note response missing 'id'"
        note_id = created_note["id"]

        # Test valid GET
        get_resp = requests.get(
            f"{BASE_URL}/note/{note_id}",
            headers=HEADERS,
            timeout=TIMEOUT
        )
        assert get_resp.status_code == 200, f"GET note failed with status {get_resp.status_code}"
        note = get_resp.json()
        assert note.get("id") == note_id, "Returned note id mismatch"
        assert note.get("title") == note_data["title"], "Returned note title mismatch"
        assert note.get("content") == note_data["content"], "Returned note content mismatch"

        # Test invalid note ID (random/likely non-existent)
        invalid_id = "nonexistent-note-id-123456"
        get_invalid_resp = requests.get(
            f"{BASE_URL}/note/{invalid_id}",
            headers=HEADERS,
            timeout=TIMEOUT
        )
        # Assuming 404 or 400 for not found
        assert get_invalid_resp.status_code in {400, 404}, f"Expected 400 or 404 for invalid note id, got {get_invalid_resp.status_code}"

        # Test unauthorized access with no token
        no_auth_resp = requests.get(
            f"{BASE_URL}/note/{note_id}",
            timeout=TIMEOUT
        )
        assert no_auth_resp.status_code in {401, 403}, f"Expected 401 or 403 for unauthorized access, got {no_auth_resp.status_code}"

        # Test unauthorized access with invalid token
        invalid_headers = HEADERS.copy()
        invalid_headers["Authorization"] = "Bearer invalid.token.here"
        invalid_auth_resp = requests.get(
            f"{BASE_URL}/note/{note_id}",
            headers=invalid_headers,
            timeout=TIMEOUT
        )
        assert invalid_auth_resp.status_code in {401, 403}, f"Expected 401 or 403 for invalid token, got {invalid_auth_resp.status_code}"

    finally:
        if note_id:
            # Clean up created note
            requests.delete(
                f"{BASE_URL}/note/{note_id}",
                headers=HEADERS,
                timeout=TIMEOUT
            )

test_get_note_by_id_with_authentication()
