from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

DATABRICKS_HOST = os.getenv("DATABRICKS_HOST")
DATABRICKS_PATH = os.getenv("DATABRICKS_PATH")
DATABRICKS_TOKEN = os.getenv("DATABRICKS_TOKEN")
DATABRICKS_CATALOG = os.getenv("DATABRICKS_CATALOG")
DATABRICKS_SCHEMA = os.getenv("DATABRICKS_SCHEMA")
DATABRICKS_URI = f"databricks://token:{DATABRICKS_TOKEN}@{DATABRICKS_HOST}?" + f"http_path={DATABRICKS_PATH}&catalog={DATABRICKS_CATALOG}&schema={DATABRICKS_SCHEMA}"

engine = None
SessionLocal = None

def create_databricks_engine():
    global engine, SessionLocal
    connect_args = {"check_same_thread": False}
    engine = create_engine(DATABRICKS_URI, connect_args=connect_args)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
        