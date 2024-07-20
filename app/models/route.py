from typing import List

from pydantic import BaseModel

from app.models.stop import Stop

class Route(BaseModel):
    name: str
    stops: List[Stop]