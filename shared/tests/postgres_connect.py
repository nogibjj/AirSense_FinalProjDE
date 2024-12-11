from sqlalchemy import create_engine

db_url = "postgresql://user:password@localhost:5432/airsense"
engine = create_engine(db_url)

with engine.connect() as connection:
    result = connection.execute("SELECT 1")
    print(result.fetchall())
