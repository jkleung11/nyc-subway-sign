from pydantic import BaseModel


class Arrival(BaseModel):
    route_id: str
    gtfs_stop_id: str
    direction_label: str
    direction_letter: str
    arrival_time: str
    arrival_mins: int
