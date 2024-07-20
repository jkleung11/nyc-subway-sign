import time
from typing import Dict, List

from google.protobuf.json_format import MessageToDict
from pydantic import BaseModel
import requests

from app.models.feed import Feed
from app.models.stop import Stop


class StopTimes(BaseModel):

    def parse_arrivals(trip_updates: List[Dict], stop: Stop, direction: str) -> List[Dict]:
        """parse list of stop time updates for a stop and direction to generate
        a list of arrivals"""
        # we need the route id for each trip update
        arrivals = []
        stop_id = stop.direction_stop_id(direction)

    @staticmethod
    def get_trip_updates(feed: Feed) -> List[Dict]:
        """make request to API for feed data and parse for trip updates"""
        try:
            resp = requests.get(feed.endpoint_url)
            resp.raise_for_status()
        except requests.exceptions.RequestException as e:
            raise Exception(
                f"error retrieving data from endpoint {feed.endpoint_url}: {e}"
            )

        feed_message = feed.feed_message()
        feed_message.ParseFromString(resp.content)
        entities = MessageToDict(feed_message)["entity"]

        trip_updates = [
            entity["tripUpdate"] for entity in entities if "tripUpdate" in entity.keys()
        ]
        
        # keep the trip update structure since we need the route
        return [
            trip_update
            for trip_update in trip_updates
            if "stopTimeUpdate" in trip_update.keys()
        ]

    @staticmethod
    def mins_to_arrival(timestamp_str: str) -> int:
        time_to_train = int(timestamp_str) - time.time()
        in_mins = int(time_to_train / 60)
        return in_mins

