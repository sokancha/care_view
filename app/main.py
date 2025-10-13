from fastapi import FastAPI

app = FastAPI(title="CareView Health Dashboard API")

@app.get("/")
def read_root():
    return {"message": "CareView API is Running! (FastAPI + Docker)"}