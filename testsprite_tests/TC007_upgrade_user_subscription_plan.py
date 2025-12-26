import requests

BASE_URL = "http://localhost:3000/api"
HEADERS = {
    "Content-Type": "application/json"
}
TIMEOUT = 30

def test_upgrade_user_subscription_plan():
    url = f"{BASE_URL}/subscription/upgrade"
    payloads = [
        {"plan": "PLUS", "callbackUrl": "https://example.com/callback/plus"},
        {"plan": "PREMIUM", "callbackUrl": "https://example.com/callback/premium"}
    ]

    for payload in payloads:
        try:
            response = requests.post(url, json=payload, headers=HEADERS, timeout=TIMEOUT)
            assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}"
        except requests.RequestException as e:
            assert False, f"Request failed: {e}"

test_upgrade_user_subscription_plan()
