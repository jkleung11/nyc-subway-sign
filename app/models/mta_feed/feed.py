import csv
from typing import Any, Dict, List, Optional

import requests
from pydantic import BaseModel
from google.transit import gtfs_realtime_pb2
from google.protobuf.json_format import MessageToDict

from metadata.constants import ROUTE_ENDPOINT_DICT

    
class Feed(BaseModel):
    """
    responsible for making requests to real time updates endpoint
    """

    routes: List[str]

    @property
    def endpoint_urls(self) -> List[str]:
        return ROUTE_ENDPOINT_DICT[self.endpoint_url]

    def get_message(self) -> dict:
        """
        request real time data from feed endpoint, returning as json
        """
        try:
            resp = requests.get(self.endpoint_url)
            resp.raise_for_status()
        except requests.exceptions.RequestException as e:
            raise Exception(f"error retrieving data from MTA feed: {e}")
        feed_message = gtfs_realtime_pb2.FeedMessage()
        feed_message.ParseFromString(resp.content)
        return MessageToDict(feed_message)

    def parse_message(message, stop: Stop, direction: str):
        """extract feed for stop updates for a stop id"""
        if direction is not direction.lower() not in ("north", "south"):
            raise ValueError("must supply stop id with direction")

