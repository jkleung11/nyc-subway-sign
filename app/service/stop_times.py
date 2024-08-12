from datetime import datetime
import time
from typing import Dict, List

from google.protobuf.json_format import MessageToDict
import httpx

from app.models.arrival import Arrivals
from app.models.stop import Stop
from app.models.feed import Feed


class StopTimes():

    async def arrivals(self, stop: Stop, feed: Feed, client: httpx.AsyncClient):
        feed_message = await self.request_feed(feed=feed, client=client)
        arrivals = self.parse_feed_message(feed_message=feed_message, stop=stop)
        return arrivals


    @staticmethod
    async def request_feed(feed: Feed, client: httpx.AsyncClient) -> List[Dict]:
        """make request to API for feed data and return entities"""
        try:
            resp = await client.get(feed.endpoint_url)
            resp.raise_for_status()
        except httpx.HTTPError as e:
            raise Exception(
                f"error retrieving data from endpoint {feed.endpoint_url}: {e}"
            )

        feed_message = feed.feed_message()
        feed_message.ParseFromString(resp.content)
        return MessageToDict(feed_message)

    def parse_feed_message(self, feed_message: List[Dict], stop: Stop) -> List:
        stop_times = []
        for entity in feed_message["entity"]:
            # only parse if there are stop times
            if "tripUpdate" not in entity.keys():
                continue
            elif "stopTimeUpdate" not in entity["tripUpdate"].keys():
                continue
            else:
                route_id = entity["tripUpdate"]["trip"]["routeId"]
                stop_time_updates = entity["tripUpdate"]["stopTimeUpdate"]
                stop_times.extend(
                    self.parse_stop_time_updates(
                        stop_time_updates, stop, route_id
                    )
                )

        return stop_times

    def parse_stop_time_updates(
        self, stop_time_updates: List[Dict], stop: Stop, route_id: str
    ) -> Dict:
        arrivals = {"N": [], "S": []}
        arrivals = []
        for stop_time in stop_time_updates:
            stop_id, direction_letter = stop_time["stopId"][:-1], stop_time["stopId"][-1]
            if stop_id != stop.gtfs_stop_id:
                continue
            # arrivals[direction_letter].append(
            arrivals.append(
                {
                    "route_id": route_id,
                    "gtfs_stop_id": stop.gtfs_stop_id,
                    "direction_label": stop.direction_label(direction_letter=direction_letter),
                    "arrival_mins": self.mins_to_train(stop_time["arrival"]["time"]),
                    "arrival_time": self.arrival_time(stop_time["arrival"]["time"])
                }
            )
        return arrivals
    
    @staticmethod
    def mins_to_train(timestamp_str: str) -> int:
        """returns arrival time in mins"""
        time_to_train = int(timestamp_str) - time.time()
        in_mins = int(time_to_train / 60)
        return in_mins
    
    @staticmethod
    def arrival_time(arrival_timestamp: str) -> str:
        # need timezone here since we're running in container
        return datetime.fromtimestamp(int(arrival_timestamp)).strftime("%H:%M")