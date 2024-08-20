from flask import Flask, jsonify, request
import requests
import time

app = Flask(__name__)

# Configuration
WINDOW_SIZE = 10
TEST_SERVER_URL = "http://20.244.56.144/test/"
TIMEOUT = 0.5  # 500 milliseconds
AUTH_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJNYXBDbGFpbXMiOnsiZXhwIjoxNzI0MTYxNzUwLCJpYXQiOjE3MjQxNjE0NTAsImlzcyI6IkFmZm9yZG1lZCIsImp0aSI6IjkyMDIyYzI5LTkyYWItNDQyMi04MzJiLTg5ODdlMjA2ZTYxNSIsInN1YiI6InBhdGVsYXl1c2gwMWphbkBnbWFpbC5jb20ifSwiY29tcGFueU5hbWUiOiJBZmZvcmQiLCJjbGllbnRJRCI6IjkyMDIyYzI5LTkyYWItNDQyMi04MzJiLTg5ODdlMjA2ZTYxNSIsImNsaWVudFNlY3JldCI6ImhjaHFDRkpVVnJObE1LRGIiLCJvd25lck5hbWUiOiJBeXVzaCBQYXRlbCIsIm93bmVyRW1haWwiOiJwYXRlbGF5dXNoMDFqYW5AZ21haWwuY29tIiwicm9sbE5vIjoiMjEwMDU2MDEwMDA0MSJ9.nW6X9Ext44RgpwJzUY-lUjLHi81CTPkF3HUOlYGuwPE"  # Replace with your actual token

# In-memory storage for the window
window = []

def fetch_numbers(number_id):
    headers = {
        "Authorization": f"Bearer {AUTH_TOKEN}"
    }
    try:
        response = requests.get(f"{TEST_SERVER_URL}/{number_id}", headers=headers, timeout=TIMEOUT)
        if response.status_code == 200:
            return response.json().get("numbers", [])
    except requests.exceptions.RequestException:
        pass
    return []

@app.route('/numbers/<number_id>', methods=['GET'])
def get_numbers(number_id):
    if number_id not in ['p', 'f', 'e', 'r']:
        return jsonify({"error": "Invalid number ID"}), 400

    # Fetch numbers from the test server
    numbers = fetch_numbers(number_id)
    if not numbers:
        return jsonify({"error": "Failed to fetch numbers"}), 500

    # Ensure numbers are unique
    unique_numbers = list(set(numbers))

    # Store the previous state of the window
    window_prev_state = window.copy()

    # Update the window with new numbers
    for num in unique_numbers:
        if num not in window:
            if len(window) >= WINDOW_SIZE:
                window.pop(0)
            window.append(num)

    # Calculate the average of the current window
    avg = sum(window) / len(window) if window else 0

    # Format the response
    response = {
        "numbers": unique_numbers,
        "windowPrevState": window_prev_state,
        "windowCurrState": window,
        "avg": round(avg, 2)
    }

    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
