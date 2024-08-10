from typing import Dict, List

from google.protobuf.json_format import MessageToDict
from pydantic import BaseModel
import httpx

from app.models.feed import Feed


class StopTimes(BaseModel):

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

    def stop_times(self, feed_message: List[Dict], gtfs_stop_id: str) -> List:
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
                        stop_time_updates, gtfs_stop_id, route_id
                    )
                )

        return stop_times

    @staticmethod
    def parse_stop_time_updates(
        stop_time_updates: List[Dict], gtfs_stop_id: str, route_id: str
    ) -> Dict:
        arrivals = []
        for stop_time in stop_time_updates:
            stop_id, direction = stop_time["stopId"][:-1], stop_time["stopId"][-1]
            if stop_id != gtfs_stop_id:
                continue
            arrivals.append(
                {
                    "route_id": route_id,
                    "gtfs_stop_id": gtfs_stop_id,
                    "direction_letter": direction,
                    "arrival_ts": stop_time["arrival"]["time"],
                }
            )
        return arrivals
