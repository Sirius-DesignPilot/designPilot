import requests

url = "http://127.0.0.1:8000/api/v1/ai/generate"
payload = {
    "prompt": "daire çiz",
    "language": "tr"
}

r = requests.post(url, json=payload)
print("Status:", r.status_code)
print("Response:", r.text)
