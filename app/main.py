from datetime import datetime

from fastapi import FastAPI

app = FastAPI()

# @app.

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/time")
async def time():
    return {"time": str(datetime.now())}

@app.get("/times/{stop_id}")
async def stop_times(stop_id: str):
    # this should just be a function call
    return {"stop-id": stop_id}