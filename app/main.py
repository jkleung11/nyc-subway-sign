from datetime import datetime
from typing import List, Dict

from fastapi import FastAPI

from app.service.subway_system import SubwaySystem

subway_system = SubwaySystem(stations_path="subway-stations.csv")
app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/routes")
async def routes():
    return {"routes": subway_system.system_routes}

@app.get("/routes/stops/{route}")
async def stops_on_route(route: str):
    return {"stops": subway_system.stops_on_route(route)}

