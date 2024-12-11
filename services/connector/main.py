from sqlalchemy import create_engine, text

# Database Connection
db_url = "postgresql://user:password@postgres:5432/airsense"
engine = create_engine(db_url)

# Schema Definition
schema = """
CREATE TABLE IF NOT EXISTS sample_table (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

# Initialize the Database 
# Make sure to run this script after the database is up and running
def init_db():
    with engine.connect() as connection:
        connection.execute(text(schema))
        print("Schema initialized successfully!")

if __name__ == "__main__":
    init_db()
