import requests

BASE_URL = "http://localhost:3000/api"
TOKEN = "l6OHQemPNaMJBCD04DTGyVuF4r4Rvy2m.JSbslKu4FiAV6LT7o2LW7yS%2FBbkTt8q3Lo8UFKaR6QE%3D"
HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}
TIMEOUT = 30


def test_update_existing_note_with_partial_data():
    # Create a new note first to update it later
    create_payload = {
        "title": "Original Title",
        "content": "Original Content"
    }
    create_resp = requests.post(f"{BASE_URL}/note/create", json=create_payload, headers=HEADERS, timeout=TIMEOUT)
    assert create_resp.status_code == 200 or create_resp.status_code == 201, f"Failed to create note: {create_resp.text}"
    note = create_resp.json()
    assert isinstance(note, dict), f"Note creation response is not a dict: {note}"
    note_id = note.get("id") or note.get("_id")
    assert note_id, f"Created note does not contain an ID, received keys: {list(note.keys())}"

    try:
        # Get original note data for comparison
        get_resp_before = requests.get(f"{BASE_URL}/note/{note_id}", headers=HEADERS, timeout=TIMEOUT)
        assert get_resp_before.status_code == 200, f"Failed to get note before update: {get_resp_before.text}"
        original_note = get_resp_before.json()
        original_title = original_note.get("title")
        original_content = original_note.get("content")

        # Update only the title of the note (partial update)
        partial_update_payload_title = {
            "title": "Updated Title"
        }
        patch_resp_title = requests.patch(f"{BASE_URL}/note/update/{note_id}", json=partial_update_payload_title, headers=HEADERS, timeout=TIMEOUT)
        assert patch_resp_title.status_code == 200, f"Failed to partially update note title: {patch_resp_title.text}"

        # Verify that title is updated and content is unchanged
        get_resp_after_title = requests.get(f"{BASE_URL}/note/{note_id}", headers=HEADERS, timeout=TIMEOUT)
        assert get_resp_after_title.status_code == 200, f"Failed to get note after title update: {get_resp_after_title.text}"
        updated_note_title = get_resp_after_title.json()
        assert updated_note_title.get("title") == "Updated Title", "Title was not updated correctly"
        assert updated_note_title.get("content") == original_content, "Content was changed unintentionally during title update"

        # Update only the content of the note (partial update)
        partial_update_payload_content = {
            "content": "Updated Content"
        }
        patch_resp_content = requests.patch(f"{BASE_URL}/note/update/{note_id}", json=partial_update_payload_content, headers=HEADERS, timeout=TIMEOUT)
        assert patch_resp_content.status_code == 200, f"Failed to partially update note content: {patch_resp_content.text}"

        # Verify that content is updated and title is unchanged
        get_resp_after_content = requests.get(f"{BASE_URL}/note/{note_id}", headers=HEADERS, timeout=TIMEOUT)
        assert get_resp_after_content.status_code == 200, f"Failed to get note after content update: {get_resp_after_content.text}"
        updated_note_content = get_resp_after_content.json()
        assert updated_note_content.get("content") == "Updated Content", "Content was not updated correctly"
        assert updated_note_content.get("title") == "Updated Title", "Title was changed unintentionally during content update"

    finally:
        # Clean up by deleting the created note
        delete_resp = requests.delete(f"{BASE_URL}/note/{note_id}", headers=HEADERS, timeout=TIMEOUT)
        assert delete_resp.status_code == 200 or delete_resp.status_code == 204, f"Failed to delete note: {delete_resp.text}"


test_update_existing_note_with_partial_data()
