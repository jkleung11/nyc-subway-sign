import asyncio
from contextlib import asynccontextmanager
from typing import List, Dict, Union

from fastapi import FastAPI, HTTPException
import httpx

from app.models import Arrival, Stop, TimesRequest
from app.service import Feeds, StopTimes, SubwaySystem
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

@app.get("/health")
def health():
    return "app is healthy"


@app.get("/routes")
def routes():
    return {"routes": app.subway_system.routes}


@app.get("/routes/{route_id}")
def stops_on_route(route_id: str) -> Dict[str, List[Stop]]:
    if route_id not in app.subway_system.routes.keys():
        raise HTTPException(status_code=404, detail=f"route_id: {route_id} not found")
    return {"stop": app.subway_system.routes[route_id].stops}


@app.get("/stops/{gtfs_stop_id}")
def stop_info(gtfs_stop_id) -> Dict[str, Stop]:
    if gtfs_stop_id not in app.subway_system.stops.keys():
        raise HTTPException(
            status_code=404, detail=f"gtfs_stop_id: {gtfs_stop_id} not found"
        )
    return {"stop": app.subway_system.stops[gtfs_stop_id]}


@app.post("/times")
async def times(times_request: TimesRequest) -> Dict[str, Union[str, List[Arrival]]]:
    stop = app.subway_system.stops[times_request.gtfs_stop_id]
    feeds = app.feeds.feeds_for_stop(stop)
    requests_tasks = [
        app.stop_times.get_arrivals(stop=stop, feed=feed, client=app.client)
        for feed in feeds
    ]

    responses = await asyncio.gather(*requests_tasks)
    return {
        "stop_name": stop.stop_name,
        "arrivals": app.stop_times.filter_arrivals(responses, times_request)
        }
