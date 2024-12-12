
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from databricks import get_db_session, create_databricks_engine

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

@app.get("/query")
def run_query(query: str, session: Session = Depends(get_db_session)):
    results = session.execute("SHOW TABLES").fetchall()
    return results
