from pydantic import BaseModel

class Arrival(BaseModel):
    route_id: str
    gtfs_stop_id: str
    direction: str
    arrival_ts: str
