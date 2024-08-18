import asyncio
from contextlib import asynccontextmanager
from typing import List, Dict

from fastapi import FastAPI, HTTPException
import httpx
from pydantic import BaseModel

from app.models.stop import Stop
from app.service.feeds import Feeds
from app.service.stop_times import StopTimes
from app.service.subway_system import SubwaySystem
from metadata.constants import ENDPOINT_ROUTE_DICT


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.client = httpx.AsyncClient()
    app.subway_system = SubwaySystem(stations_path="subway-stations.csv")
    app.stop_times = StopTimes()
    app.feeds = Feeds(ENDPOINT_ROUTE_DICT)
    yield
    await app.client.aclose()

app = FastAPI(lifespan=lifespan)

@app.get("/")
def root():
    return "hello world"

@app.get("/routes")
def routes():
    return {"routes": app.subway_system.system_routes}

@app.get("/routes/{route}")
def stops_on_route(route_id: str) -> List[Stop]:
    if route_id not in app.subway_system.routes.keys():
        raise HTTPException(status_code=404, detail=f"route_id: {route_id} not found")
    return app.subway_system.routes[route_id].stops

@app.get("/stops/{gtfs_stop_id}")
def stop_info(gtfs_stop_id) -> Stop:
    if gtfs_stop_id not in app.subway_system.stops.keys():
        raise HTTPException(status_code=404, detail=f"gtfs_stop_id: {gtfs_stop_id} not found")
    return app.subway_system.stops[gtfs_stop_id]


class TimesRequest(BaseModel):
    gtfs_stop_id: str
    min_mins: int = 0
    max_mins: int = 15

@app.post("/times")
async def times(times_request: TimesRequest):
    stop = app.subway_system.stops[times_request.gtfs_stop_id]
    feeds = app.feeds.feeds_for_stop(stop)
    requests_tasks = [app.stop_times.get_arrivals(stop=stop, feed=feed, client=app.client) for feed in feeds]
    arrivals_lists = await asyncio.gather(*requests_tasks)
    
    response_dict = {'N': [], 'S': []}
    
    for arrivals in arrivals_lists:
        for arrival in arrivals:
            if times_request.min_mins <= arrival.arrival_mins <= times_request.max_mins:
                response_dict[arrival.direction_letter].append(arrival)

    response_dict = {direction: sorted(arrivals, key=lambda arrival: arrival.arrival_mins) for direction, arrivals in response_dict.items()}
    return response_dict