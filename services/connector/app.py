from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import text, MetaData, Table
from sqlalchemy.orm import Session
from databricks_util import get_db_session, create_databricks_engine
from rds_util import get_rds_session, create_rds_engine
from concurrent.futures import ThreadPoolExecutor
from contextlib import asynccontextmanager
import asyncio
import pandas as pd

executor = ThreadPoolExecutor(max_workers=20)  # Configure max workers based on your needs

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_databricks_engine()
    create_rds_engine()
    print("Startup checklist finished")
    yield
    print("Shutdown checklist finished")

app = FastAPI(lifespan=lifespan)

@app.get("/")
def read_root():
    return {"version": "v0.1"}

async def run_query(session: Session, query: str):
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(executor, session.execute, text(query))
    return result.fetchall()

@app.post("/transfer_table")
async def transfer_table(
    table_name: str,
    db_session: Session = Depends(get_db_session),
    rds_session: Session = Depends(get_rds_session)
):
    try:
        # Step 1: Validate the table name
        if not table_name:
            raise HTTPException(status_code=400, detail="Table name is required.")
        
        # Step 2: Drop the table in RDS if it exists
        drop_query = f"DROP TABLE IF EXISTS {table_name}"
        rds_session.execute(text(drop_query))
        rds_session.commit()
        print(f"Table {table_name} dropped from RDS (if it existed).")

        # Step 3: Fetch data in chunks from Databricks
        chunk_size = 5000
        offset = 0
        total_rows_transferred = 0
        column_names = None

        while True:
            query = f"SELECT * FROM {table_name} LIMIT {chunk_size} OFFSET {offset}"
            databricks_result = await run_query(db_session, query)
            
            if not databricks_result:  # Break if no more rows
                break

            # Get column names for the first batch
            if column_names is None:
                columns_query = f"DESCRIBE {table_name}"
                databricks_columns = await run_query(db_session, columns_query)
                column_names = [col[0] for col in databricks_columns]

            # Convert batch to DataFrame
            df = pd.DataFrame(databricks_result, columns=column_names)

            # Step 4: Write data to RDS
            df.to_sql(
                table_name,
                con=rds_session.bind,
                if_exists="append",  # Append as the table was dropped initially
                index=False,
                method="multi"
            )

            total_rows_transferred += len(df)
            offset += chunk_size

        return {
            "status": "Table transferred successfully",
            "table_name": table_name,
            "rows_transferred": total_rows_transferred,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during table transfer: {str(e)}")


@app.get("/dbstatus")
async def read_dbstatus(session: Session = Depends(get_db_session)):
    try:
        query = "SELECT version();"
        result = await run_query(session, query)
        return {"Databricks is connected": True, "result": str(result)}
    except Exception as e:
        return {"Databricks is connected": False, "error": str(e)}

@app.get("/rdsstatus")
async def read_rdsstatus(session: Session = Depends(get_rds_session)):
    try:
        query = "SELECT version();"
        result = await run_query(session, query)
        return {"RDS is connected": True, "result": str(result)}
    except Exception as e:
        return {"RDS is connected": False, "error": str(e)}