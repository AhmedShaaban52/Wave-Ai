import requests

BASE_URL = "http://localhost:3000/api"
TOKEN = "l6OHQemPNaMJBCD04DTGyVuF4r4Rvy2m.JSbslKu4FiAV6LT7o2LW7yS%2FBbkTt8q3Lo8UFKaR6QE%3D"
HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

def test_create_new_note_with_valid_data():
    url_create = f"{BASE_URL}/note/create"
    note_data = {
        "title": "Test Note Title",
        "content": "This is the content of the test note."
    }

    response = requests.post(url_create, json=note_data, headers=HEADERS, timeout=30)
    assert response.status_code == 200 or response.status_code == 201, f"Unexpected status code: {response.status_code}"
    resp_json = response.json()

    # Verify response contains the correct data
    assert resp_json.get("title") == note_data["title"], "Title in response does not match request"
    assert resp_json.get("content") == note_data["content"], "Content in response does not match request"


test_create_new_note_with_valid_data()
