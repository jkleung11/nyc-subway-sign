from contextlib import asynccontextmanager
from typing import List, Dict

from fastapi import FastAPI, Request, HTTPException
import httpx

from app.models.stop import Stop
from app.models.feed import Feed
from app.service.stop_times import StopTimes
from app.service.subway_system import SubwaySystem
from metadata.constants import ROUTE_ENDPOINT_DICT


subway_system = SubwaySystem(stations_path="subway-stations.csv")
ace_feed = Feed(endpoint_url=ROUTE_ENDPOINT_DICT['A'])
stop_times = StopTimes()


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.client = httpx.AsyncClient()
    app.subway_system = SubwaySystem(stations_path="subway-stations.csv")
    app.stop_times = StopTimes()
    yield
    await app.client.aclose()

app = FastAPI(lifespan=lifespan)

@app.get("/")
async def root():
    return "hello world"

@app.get("/routes")
async def routes():
    return {"routes": subway_system.system_routes}

@app.get("/routes/{route}")
async def stops_on_route(route_id: str) -> List[Stop]:
    if route_id not in subway_system.routes.keys():
        raise HTTPException(status_code=404, detail=f"route_id: {route_id} not found")
    return subway_system.routes[route_id].stops

@app.get("/stops/{gtfs_stop_id}")
async def stop_info(gtfs_stop_id) -> Stop:
    if gtfs_stop_id not in subway_system.stops.keys():
        raise HTTPException(status_code=404, detail=f"gtfs_stop_id: {gtfs_stop_id} not found")
    return subway_system.stops[gtfs_stop_id]

@app.get("/times/{gtfs_stop_id}")
async def times(gtfs_stop_id: str) -> List:
    # how to know what feeds to use based on stop
    stop = app.subway_system.stops[gtfs_stop_id]
    # need to know feeds
    feed_message = await app.stop_times.request_feed(ace_feed, app.client)
    stop_times = app.stop_times.stop_times(feed_message, gtfs_stop_id)