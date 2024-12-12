from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from databricks_util import get_db_session, create_databricks_engine
from rds_util import get_rds_session, create_rds_engine, create_service_transfer_table
from concurrent.futures import ThreadPoolExecutor
from contextlib import asynccontextmanager
import asyncio
import pandas as pd

executor = ThreadPoolExecutor(max_workers=20)  # Configure max workers based on your needs

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize Databricks and RDS engines
    create_databricks_engine()
    create_rds_engine()
    try:
        create_service_transfer_table()
        print("Startup checklist finished: All systems initialized and verified.")
    except Exception as e:
        print(f"Error during startup: {e}")
        raise
    yield  # Application startup complete
    print("Shutdown checklist finished")


app = FastAPI(lifespan=lifespan)


@app.get("/")
def read_root():
    return {"version": "v0.1"}


async def run_query(session: Session, query: str):
    """Run a query asynchronously using a thread pool."""
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(executor, session.execute, text(query))
    return result.fetchall()


async def drop_table_if_exists(table_name: str, rds_session: Session):
    """Drop the table in RDS if it exists."""
    drop_query = f"DROP TABLE IF EXISTS {table_name}"
    rds_session.execute(text(drop_query))
    rds_session.commit()
    print(f"Table {table_name} dropped from RDS (if it existed).")


async def fetch_data_from_databricks(table_name: str, chunk_size: int, offset: int, db_session: Session):
    """Fetch a chunk of data from Databricks."""
    query = f"SELECT * FROM {table_name} LIMIT {chunk_size} OFFSET {offset}"
    return await run_query(db_session, query)


async def get_column_names(table_name: str, db_session: Session):
    """Fetch column names for the given table."""
    columns_query = f"DESCRIBE {table_name}"
    databricks_columns = await run_query(db_session, columns_query)
    return [col[0] for col in databricks_columns]


def record_table_transfer(table_name: str, rds_session: Session):
    """Record the table transfer in the `service_transfer` table."""
    transfer_record_query = """
        INSERT INTO service_transfer (tablename, last_transfer_date, transfer_count)
        VALUES (:tablename, NOW(), 1)
        ON CONFLICT (tablename)
        DO UPDATE SET
            last_transfer_date = NOW(),
            transfer_count = service_transfer.transfer_count + 1;
    """
    rds_session.execute(
        text(transfer_record_query),
        {"tablename": table_name}
    )
    rds_session.commit()


@app.post("/transfer_table")
async def transfer_table(
    table_name: str,
    db_session: Session = Depends(get_db_session),
    rds_session: Session = Depends(get_rds_session)
):
    try:
        # Validate table name
        if not table_name:
            raise HTTPException(status_code=400, detail="Table name is required.")

        # Drop the table if it exists
        await drop_table_if_exists(table_name, rds_session)

        # Initialize data transfer variables
        chunk_size = 5000
        offset = 0
        total_rows_transferred = 0
        column_names = None

        while True:
            # Fetch data in chunks
            databricks_result = await fetch_data_from_databricks(table_name, chunk_size, offset, db_session)

            if not databricks_result:  # Break if no more rows
                break

            # Get column names for the first batch
            if column_names is None:
                column_names = await get_column_names(table_name, db_session)

            # Convert batch to DataFrame
            df = pd.DataFrame(databricks_result, columns=column_names)

            # Write data to RDS
            df.to_sql(
                table_name,
                con=rds_session.bind,
                if_exists="append",  # Append as the table was dropped initially
                index=False,
                method="multi"
            )

            total_rows_transferred += len(df)
            offset += chunk_size

        # Record the transfer in the `service_transfer` table
        record_table_transfer(table_name, rds_session)

        return {
            "status": "Table transferred successfully",
            "table_name": table_name,
            "rows_transferred": total_rows_transferred,
        }

    except SQLAlchemyError as e:
        rds_session.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during table transfer: {str(e)}")


@app.get("/dbstatus")
async def read_dbstatus(session: Session = Depends(get_db_session)):
    """Check Databricks database connection."""
    try:
        query = "SELECT version();"
        result = await run_query(session, query)
        return {"Databricks is connected": True, "result": str(result)}
    except Exception as e:
        return {"Databricks is connected": False, "error": str(e)}


@app.get("/rdsstatus")
async def read_rdsstatus(session: Session = Depends(get_rds_session)):
    """Check RDS database connection."""
    try:
        query = "SELECT version();"
        result = await run_query(session, query)
        return {"RDS is connected": True, "result": str(result)}
    except Exception as e:
        return {"RDS is connected": False, "error": str(e)}
