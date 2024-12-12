from databricks import sql
from dotenv import load_dotenv
import os

# Load .env file from the root directory dynamically
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
load_dotenv(dotenv_path=os.path.join(root_dir, ".env"))

# Fetch environment variables
DATABRICKS_HOST = os.getenv("DATABRICKS_HOST")
DATABRICKS_PATH = os.getenv("DATABRICKS_PATH")
DATABRICKS_TOKEN = os.getenv("DATABRICKS_TOKEN")

try:
    with sql.connect(server_hostname = DATABRICKS_HOST,
                    http_path       = DATABRICKS_PATH,
                    access_token    = DATABRICKS_TOKEN) as connection:
        # Add your database operations here
        print("Connected to the database successfully.")
except Exception as e:
    print("Error connecting to the database:", e)
    if 'timeout expired' in str(e):
        print("Connection attempt timed out. Please check your network and database server.")
