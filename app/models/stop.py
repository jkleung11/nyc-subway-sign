from typing import List, Optional

from pydantic import BaseModel


class Stop(BaseModel):
    """
    represents an individual stop within the system.
    stop id values returned from realtime feeds have N or S as its last character,
    denoting if the stop is the Northbound or Southbound side.
    """

    station_id: int # lower id means uptown, higher is downtown
    gtfs_stop_id: str
    stop_name: str
    routes: List[str]
    north_direction_label: Optional[str]
    south_direction_label: Optional[str]

    @property
    def direction_stop_id(self, direction: str) -> str:
        if direction.lower() not in ("north", "south"):
            raise ValueError("direction must be either north or south")
        direction_stop_ids = {
            "north": self.gtfs_stop_id + "N",
            "south": self.gtfs_stop_id + "S",
        }
        return direction_stop_ids[direction]
