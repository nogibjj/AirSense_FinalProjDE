from sqlalchemy import create_engine, text
import os

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

# Initialize the Database 
# Make sure to run this script after the database is up and running
def init_db():
    # Create the SQLAlchemy connection string
    connection_string = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

    # Create an SQLAlchemy engine
    engine = create_engine(connection_string)

    # Test the connection
    try:
        with engine.connect() as connection:
            # Wrap the query in text()
            result = connection.execute(text("SELECT version();"))
            for row in result:
                print("Database Version:", row[0])
    except Exception as e:
        print("Error connecting to the database:", e)


if __name__ == "__main__":
    init_db()
