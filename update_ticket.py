import requests
import json

# Update Bug Ticket #2 status to 'fixed'
url = "http://localhost:8000/api/update-status/"
payload = {
    "ticket_id": 2,
    "status": "fixed"
}

try:
    response = requests.post(url, json=payload)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
except Exception as e:
    print(f"Error: {e}")

# Made with Bob
