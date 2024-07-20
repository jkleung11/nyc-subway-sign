from datetime import datetime
from typing import List, Dict

from fastapi import FastAPI

# from app.models.feed import Feed
# from app.service.stop_times import FeedParser
from app.service.subway_system import SubwaySystem


subway_system = SubwaySystem(stations_path="subway-stations.csv")
# feeds = {}

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/routes")
async def routes():
    return {"routes": subway_system.system_routes}


@app.get("/routes/{route}/stops")
async def stops_on_route(route: str):
    return {"stops": subway_system.routes[route].stops}
