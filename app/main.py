from typing import List, Dict

from fastapi import FastAPI

from app.models.stop import Stop
from app.models.feed import Feed
from app.service.stop_times import StopTimes
from app.service.subway_system import SubwaySystem
from metadata.constants import ROUTE_ENDPOINT_DICT


subway_system = SubwaySystem(stations_path="subway-stations.csv")
ace_feed = Feed(endpoint_url=ROUTE_ENDPOINT_DICT['A'])
stop_times = StopTimes()

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/routes")
async def routes():
    return {"routes": subway_system.system_routes}


@app.get("/routes/{route}/stops")
async def stops_on_route(route: str) -> List[Stop]:
    return subway_system.routes[route].stops

@app.get("/times/{gtfs_stop_id}")
async def times(gtfs_stop_id: str) -> List:
    feed_message = stop_times.request_feed(ace_feed)
    return stop_times.arrivals(feed_message, gtfs_stop_id)