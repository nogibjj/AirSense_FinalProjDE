from flask import Flask, jsonify

app = Flask(__name__)

# Sample data
tasks = [
    {"id": 1, "title": "Do the laundry", "completed": False},
    {"id": 2, "title": "Write Flask app", "completed": True},
]

@app.route('/')
def home():
    return "Welcome to AirSense API gateway!"

# Get all tasks
@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify(tasks)


if __name__ == '__main__':
    app.run(debug=True)
