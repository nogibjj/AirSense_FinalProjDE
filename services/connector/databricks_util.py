from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import URL
import os
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Globals
engine = None
SessionLocal = None


def validate_env_vars():
    required_vars = [
        "DATABRICKS_HOST",
        "DATABRICKS_PATH",
        "DATABRICKS_TOKEN",
        "DATABRICKS_CATALOG",
        "DATABRICKS_SCHEMA",
    ]
    for var in required_vars:
        if not os.getenv(var):
            raise EnvironmentError(f"Environment variable {var} is not set.")


def create_databricks_engine():
    global engine, SessionLocal
    validate_env_vars()

    DATABRICKS_URI = URL.create(
        drivername="databricks",
        username="token",
        password=os.getenv("DATABRICKS_TOKEN"),
        host=os.getenv("DATABRICKS_HOST"),
        query={
            "http_path": os.getenv("DATABRICKS_PATH"),
            "catalog": os.getenv("DATABRICKS_CATALOG"),
            "schema": os.getenv("DATABRICKS_SCHEMA"),
        },
    )
    engine = create_engine(DATABRICKS_URI)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    # Test the connection
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1")).scalar()
            if result == 1:
                logger.info("Connection to Databricks is successful.")
            else:
                logger.error("Connection test query did not return expected result.")
    except Exception as e:
        logger.error(f"Error during Databricks connection test: {e}")
        raise  # Stop execution if the connection test fails


def get_db_session():
    if not SessionLocal:
        raise RuntimeError(
            "SessionLocal is not initialized. Call `create_databricks_engine()` first."
        )
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
