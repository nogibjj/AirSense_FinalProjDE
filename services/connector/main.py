from sqlalchemy import create_engine, text
import os


def connect_rds(engine):
    """
    Connect to the RDS database and print the version
    """
    try:
        with engine.connect() as connection:
            # Wrap the query in text()
            result = connection.execute(text("SELECT version();"))
            for row in result:
                print("RDS is connected! Database Version:", row[0])
            return connection
    except Exception as e:
        print("Error connecting to the database:", e)


def main():

    # CONNECT TO RDS POSTGRES DATABASE
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT")
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_NAME = os.getenv("DB_NAME")

    # Create the SQLAlchemy connection string
    connection_string = (
        f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )
    # Create an SQLAlchemy engine
    engine = create_engine(connection_string)
    conn = connect_rds(engine)
    result = conn.execute(text("SELECT version();"))
    for row in result:
        print("RDS is connected! Database Version:", row[0])


if __name__ == "__main__":
    main()
