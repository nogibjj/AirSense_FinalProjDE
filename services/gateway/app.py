from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import text
from app.gateway_utils import validate_env_vars

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

@app.route("/tables", methods=["GET"])
def list_tables():
    """
    A route to display all the tables in the database.
    """
    try:
        # Get the list of table names from the database
        tables = db.session.execute(text("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';"))
        return render_template("tables.html", tables=tables)
    except Exception as e:
        return jsonify({"message": "Failed to retrieve tables!", "error": str(e)}), 500
    
@app.route("/airline_performance", methods=["GET"])
def get_airline_performance():
    """
    A route to retrieve the airline performance data.
    """
    try:
        # Execute the query and fetch all results
        query = text("SELECT * FROM airline_performance;")
        result = db.session.execute(query)
        rows = result.fetchall()
        
        # Dynamically retrieve column names
        column_names = result.keys()

        # Convert rows into a list of dictionaries, matching columns to values
        performance_data = [dict(zip(column_names, row)) for row in rows]

        return jsonify(performance_data)
    except Exception as e:
        return jsonify({"message": "Failed to retrieve airline performance data!", "error": str(e)}), 500




if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
