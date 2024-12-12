import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session
from databricks_util import get_db_session, create_databricks_engine

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

@app.get("/dbstatus")
def read_dbstatus(session: Session = Depends(get_db_session)):
    try:
        query = session.execute(text("SELECT * FROM airline_performance LIMIT 5"))
        result = query.fetchall()

        return {"Databricks is connected": True, "result": str(result)}
    except Exception as e:
        return {"Databricks is connected": False, "error": str(e)}
