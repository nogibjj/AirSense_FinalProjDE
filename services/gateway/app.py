from flask import Flask, jsonify
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({'message': 'Welcome to the AirSense!'})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
