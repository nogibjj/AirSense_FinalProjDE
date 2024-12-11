import psycopg2
from psycopg2 import OperationalError
from dotenv import load_dotenv
import os

# Load .env file from the root directory dynamically
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
load_dotenv(dotenv_path=os.path.join(root_dir, ".env"))

# Fetch environment variables
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

try:
    print("Connecting to the database...")
    print(f"Host: {DB_HOST}, Port: {DB_PORT}, User: {DB_USER}, Database: {DB_NAME}")
    # Establish connection
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        connect_timeout=5  # Set timeout to 5 seconds
    )
    
    # Create a cursor
    cursor = conn.cursor()
    
    # Example query
    cursor.execute("SELECT version();")
    result = cursor.fetchone()
    print("Database Version:", result)
    
    # Close cursor and connection
    cursor.close()
    conn.close()
except OperationalError as e:
    print("Error connecting to the database:", e)
    if 'timeout expired' in str(e):
        print("Connection attempt timed out. Please check your network and database server.")
