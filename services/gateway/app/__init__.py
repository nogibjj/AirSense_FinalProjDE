import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

from .gateway_utils import validate_env_vars
from openai import OpenAI


# Define a base class for SQLAlchemy models
class Base(DeclarativeBase):
    pass

# Initialize SQLAlchemy with the custom base model
db = SQLAlchemy(model_class=Base)

def create_app():
    app = Flask(__name__, template_folder="../templates", static_folder="../static")
    # Retrieve PostgreSQL URI from environment variables or another validation source
    pg_uri = validate_env_vars()
    # Configure the PostgreSQL database connection
    app.config["SQLALCHEMY_DATABASE_URI"] = pg_uri
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    # Initialize SQLAlchemy with the app
    db.init_app(app)
    # Initialize the OpenAI client
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    # Register routes
    from .api_routes import create_api_routes
    from .html_routes import create_html_routes
    # Register Blueprints
    app.register_blueprint(create_api_routes(db, client))
    app.register_blueprint(create_html_routes(db))

    return app
