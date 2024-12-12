from sqlalchemy import create_engine, text, inspect
from sqlalchemy.orm import sessionmaker
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
        "DB_HOST",
        "DB_PORT",
        "DB_USER",
        "DB_PASSWORD",
        "DB_NAME",
    ]
    for var in required_vars:
        if not os.getenv(var):
            raise EnvironmentError(f"Environment variable {var} is not set.")


def create_rds_engine():
    global engine, SessionLocal
    validate_env_vars()

    RDS_URI = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"

    engine = create_engine(RDS_URI)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    # Test the connection
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1")).scalar()
            if result == 1:
                logger.info("Connection to RDS is successful.")
            else:
                logger.error("Connection test query did not return expected result.")
    except Exception as e:
        logger.error(f"Error during RDS connection test: {e}")
        raise  # Stop execution if the connection test fails


def create_service_transfer_table():
    """
    Check if the `service_transfer` table exists in the `public` schema,
    and create it if not.
    """
    if not engine:
        raise RuntimeError(
            "Engine is not initialized. Call `create_rds_engine()` first."
        )

    with engine.connect() as connection:
        inspector = inspect(engine)
        schema = "public"  # Adjust this if using a different schema
        logger.info(
            f"Existing tables in schema '{schema}': "
            f"{inspector.get_table_names(schema=schema)}"
        )

        if "service_transfer" not in inspector.get_table_names(schema=schema):
            logger.info("`service_transfer` table does not exist. Creating it now.")
            create_table_query = f"""
            CREATE TABLE {schema}.service_transfer (
                id SERIAL PRIMARY KEY,
                tablename VARCHAR(255) NOT NULL UNIQUE,
                last_transfer_date TIMESTAMP NOT NULL,
                transfer_count INT NOT NULL DEFAULT 1
            );
            """
            transaction = connection.begin()
            try:
                connection.execute(text(create_table_query))
                transaction.commit()
                logger.info("`service_transfer` table created successfully.")
            except Exception as e:
                transaction.rollback()
                logger.error(f"Error creating `service_transfer` table: {e}")
                raise
        else:
            logger.info("`service_transfer` table already exists.")


def get_rds_session():
    if not SessionLocal:
        raise RuntimeError(
            "SessionLocal is not initialized. Call `create_rds_engine()` first."
        )
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
