import asyncio
from contextlib import asynccontextmanager
from typing import List, Dict

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


@app.get("/routes")
def routes():
    return {"routes": app.subway_system.system_routes}


@app.get("/routes/{route_id}")
def stops_on_route(route_id: str) -> List[Stop]:
    if route_id not in app.subway_system.routes.keys():
        raise HTTPException(status_code=404, detail=f"route_id: {route_id} not found")
    return app.subway_system.routes[route_id].stops


@app.get("/stops/{gtfs_stop_id}")
def stop_info(gtfs_stop_id) -> Stop:
    if gtfs_stop_id not in app.subway_system.stops.keys():
        raise HTTPException(
            status_code=404, detail=f"gtfs_stop_id: {gtfs_stop_id} not found"
        )
    return app.subway_system.stops[gtfs_stop_id]


@app.post("/times")
async def times(times_request: TimesRequest) -> Dict[str, List[Arrival]]:
    stop = app.subway_system.stops[times_request.gtfs_stop_id]
    feeds = app.feeds.feeds_for_stop(stop)
    requests_tasks = [
        app.stop_times.get_arrivals(stop=stop, feed=feed, client=app.client)
        for feed in feeds
    ]
    
    responses = await asyncio.gather(*requests_tasks)

    times_dict = {"N": [], "S": []}

    for arrivals in responses:
        for arrival in arrivals:
            if times_request.min_mins <= arrival.arrival_mins <= times_request.max_mins:
                times_dict[arrival.direction_letter].append(arrival)

    times_dict = {
        direction: sorted(arrivals, key=lambda arrival: arrival.arrival_mins)
        for direction, arrivals in times_dict.items()
    }
    return times_dict
