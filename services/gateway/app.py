from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import text
from gateway_utils import validate_env_vars

# Define a base class for SQLAlchemy models
class Base(DeclarativeBase):
    pass

# Initialize SQLAlchemy with the custom base model
db = SQLAlchemy(model_class=Base)

# Create the Flask app
app = Flask(__name__)

# Retrieve PostgreSQL URI from environment variables or another validation source
pg_uri = validate_env_vars()
# Configure the PostgreSQL database connection
app.config["SQLALCHEMY_DATABASE_URI"] = pg_uri
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize the database with the Flask app
db.init_app(app)

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Hello, world!"})

@app.route("/hello", methods=["GET"])
def hello():
    """
    A test endpoint to verify the application is running
    and the database connection is configured.
    """
    try:
        # Test the connection using a session
        version = db.session.execute(text("SELECT version();"))
        return jsonify({"message": "Database connection successful!", "version": version.scalar()})
    except Exception as e:
        return jsonify({"message": "Database connection failed!", "error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
