from fastapi import FastAPI
from src.backend.api.endpoints import contracts
from fastapi.staticfiles import StaticFiles

app = FastAPI()



app.include_router(contracts.router, prefix="/api")

app.mount("/", StaticFiles(directory="src/frontend/public", html=True), name="static")

@app.get("/")
def read_root():
    return {"message": "Welcome to the Contract Validation API"}