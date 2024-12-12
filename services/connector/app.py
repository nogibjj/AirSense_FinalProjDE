from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session
from databricks_util import get_db_session, create_databricks_engine
from concurrent.futures import ThreadPoolExecutor
import asyncio

executor = ThreadPoolExecutor(max_workers=20)  # Configure max workers based on your needs

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_databricks_engine()
    print("Startup checklist finished")
    yield
    print("Shutdown checklist finished")

app = FastAPI(lifespan=lifespan)

@app.get("/")
def read_root():
    return {"Hello": "World"}

async def run_query(session: Session, query: str):
    # Run the query in a thread pool to avoid blocking
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(executor, session.execute, text(query))
    return result.fetchall()

@app.get("/dbstatus")
async def read_dbstatus(session: Session = Depends(get_db_session)):
    try:
        query = "SELECT * FROM airline_performance LIMIT 5"
        result = await run_query(session, query)

        return {"Databricks is connected": True, "result": str(result)}
    except Exception as e:
        return {"Databricks is connected": False, "error": str(e)}

