import time
from pydantic import BaseModel


class Arrival(BaseModel):
    route_id: str
    direction: str
    arrival_ts: str

    @property
    def arrival_mins(self) -> int:
        return int(time.time() - int(self.arrival_ts))
