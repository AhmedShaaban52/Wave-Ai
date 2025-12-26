import requests

BASE_URL = "http://localhost:3000/api"
TOKEN = "l6OHQemPNaMJBCD04DTGyVuF4r4Rvy2m.JSbslKu4FiAV6LT7o2LW7yS%2FBbkTt8q3Lo8UFKaR6QE%3D"
HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}
TIMEOUT = 30


def test_delete_note_with_valid_authentication():
    note_create_url = f"{BASE_URL}/note/create"
    note_url_template = f"{BASE_URL}/note/{{}}"

    # Step 1: Create a new note to delete
    note_data = {
        "title": "Test Note to Delete",
        "content": "This note will be deleted in the test."
    }

    response_create = requests.post(note_create_url, json=note_data, headers=HEADERS, timeout=TIMEOUT)
    assert response_create.status_code == 200 or response_create.status_code == 201, f"Failed to create note, status code: {response_create.status_code}"
    note = response_create.json()
    note_id = note.get('id')
    assert note_id is not None, f"Created note ID is missing in response: {note}"

    try:
        # Step 2: Delete the created note
        delete_url = note_url_template.format(note_id)
        response_delete = requests.delete(delete_url, headers=HEADERS, timeout=TIMEOUT)
        assert response_delete.status_code == 200 or response_delete.status_code == 204, f"Failed to delete note, status code: {response_delete.status_code}"

        # Step 3: Verify the note is removed and cannot be accessed
        response_get = requests.get(delete_url, headers=HEADERS, timeout=TIMEOUT)
        # Expecting 404 Not Found or similar error because note should no longer exist
        assert response_get.status_code == 404 or response_get.status_code == 400 or response_get.status_code == 410, \
            f"Deleted note still accessible, status code: {response_get.status_code}"

    finally:
        # Cleanup in case note was not deleted
        requests.delete(note_url_template.format(note_id), headers=HEADERS, timeout=TIMEOUT)


test_delete_note_with_valid_authentication()
