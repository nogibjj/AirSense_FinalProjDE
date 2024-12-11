import psycopg2
from psycopg2 import OperationalError

# Connection details
HOST = 'airsense-pg.cluster-cnwm886wwadv.us-east-1.rds.amazonaws.com'
PORT = 3306
DATABASE = 'airsense'
USER = 'postgres'
PASSWORD = '' # Enter your password here

try:
    # Establish connection
    conn = psycopg2.connect(
        host=HOST,
        port=PORT,
        database=DATABASE,
        user=USER,
        password=PASSWORD,
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
