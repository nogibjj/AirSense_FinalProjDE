from flask import Blueprint, jsonify

gate = Blueprint('gate', __name__)

@gate.route('/')
def home():
    return jsonify({'message': 'Welcome to the AirSense!'})

@gate.route('/hello/<name>')
def hello(name):
    return jsonify({'message': f'Hello, {name}!'})
