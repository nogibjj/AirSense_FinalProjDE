from sqlalchemy import create_engine, text
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

def get_rds_session():
    if not SessionLocal:
        raise RuntimeError("SessionLocal is not initialized. Call `create_rds_engine()` first.")
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
