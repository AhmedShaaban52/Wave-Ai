import requests
import uuid

BASE_URL = "http://localhost:3000/api"


# Use a session to handle session-based authentication
session = requests.Session()

# Assuming login is required before accessing the endpoints; however, no login API here,
# so simulate session with cookie if possible or just remove Authorization header as per PRD.


def test_send_chat_message_and_receive_ai_response():
    url = f"{BASE_URL}/chat"

    payload = {
        "id": str(uuid.uuid4()),
        "message": {
            "text": "Hello AI, please respond!"
        },
        "selectedModelId": "gpt-4",
        "selectedToolName": None
    }

    try:
        # Send without Authorization header, assuming session-based auth is handled externally
        response = session.post(url, json=payload, timeout=30)
        # Assert status code 200 OK
        assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"

        data = response.json()
        # Assert there is an AI response in the returned data and it contains expected keys
        assert isinstance(data, dict), "Response JSON is not a dict"
        # Assuming response contains a key like 'reply' or 'message' as AI response
        assert "reply" in data or "message" in data, "Response does not contain AI reply/message"

        # If 'reply' exists, verify it's a non-empty string
        if "reply" in data:
            assert isinstance(data["reply"], str) and data["reply"].strip() != "", "AI reply is empty or not a string"

        # If 'message' exists, verify it is a dict with expected structure
        if "message" in data:
            assert isinstance(data["message"], dict), "AI message is not an object"
            # Possibly check it has 'text' or similar key
            assert "text" in data["message"], "AI message object does not contain 'text' key"
            assert isinstance(data["message"]["text"], str) and data["message"]["text"].strip() != "", "AI message text is empty or not a string"

    except requests.RequestException as e:
        assert False, f"Request failed: {e}"


test_send_chat_message_and_receive_ai_response()
