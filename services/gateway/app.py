from flask import Flask, jsonify
import requests

# Base URL for the connector service
CONNECTOR_BASE_URL = "http://connector:8000"

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({'message': 'Welcome to the AirSense!'})

@app.route('/connector')
def hello():
    try:
        # Send a GET request to the connector's root endpoint
        response = requests.get(f"{CONNECTOR_BASE_URL}/")
        response.raise_for_status()  # Raise an exception for HTTP errors

        # Parse the response JSON and include it in the gateway's response
        connector_response = response.json()
        return jsonify({'message': f'Hello from the connector!', 'connector': connector_response})
    except requests.exceptions.RequestException as e:
        # Handle errors (e.g., connector service unavailable)
        return jsonify({'message': 'Failed to connect to the connector service.', 'error': str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
