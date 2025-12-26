import requests

def test_health_check_endpoint_authentication():
    base_url = "http://localhost:3000"
    url = f"{base_url}/"
    headers = {
        "Authorization": "Bearer l6OHQemPNaMJBCD04DTGyVuF4r4Rvy2m.JSbslKu4FiAV6LT7o2LW7yS%2FBbkTt8q3Lo8UFKaR6QE%3D"
    }
    timeout = 30

    try:
        response = requests.get(url, headers=headers, timeout=timeout)
    except requests.RequestException as e:
        assert False, f"Request failed: {e}"

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
    # No specific response body is defined in PRD for health check,
    # so only checking for 200 status is sufficient.

test_health_check_endpoint_authentication()