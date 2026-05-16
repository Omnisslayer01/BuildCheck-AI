import requests
import json

# Report to boss that ticket 1 is fixed
url = "http://localhost:8000/api/update-status/"
data = {
    "ticket_id": 1,
    "status": "fixed"
}

try:
    response = requests.post(url, json=data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Error: {e}")

# Made with Bob