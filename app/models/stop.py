from typing import List, Optional

from pydantic import BaseModel


class Stop(BaseModel):
    """
    represents an individual stop within the system.
    stop id values returned from realtime feeds have N or S as its last character,
    denoting if the stop is the Northbound or Southbound side.
    """

    gtfs_stop_id: str
    stop_name: str
    routes: List[str]
    north_direction_label: Optional[str]
    south_direction_label: Optional[str]

    def direction_label(self, direction_letter: str) -> str:
        return {"N": self.north_direction_label, "S": self.south_direction_label}.get(
            direction_letter
        )
