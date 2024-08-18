from pydantic import BaseModel

class TimesRequest(BaseModel):
    gtfs_stop_id: str
    min_mins: int = 0
    max_mins: int = 15