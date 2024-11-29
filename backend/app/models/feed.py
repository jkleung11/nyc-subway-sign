from typing import List

from pydantic import BaseModel
from google.transit import gtfs_realtime_pb2


class Feed(BaseModel):
    """
    wrapper for FeedMessage protocol, includes attributes for the endpoint
    and its corresponding routes
    """

    endpoint_url: str
    routes: List[str]

    def has_routes(self, routes_list: List[str]) -> bool:
        "checks if the feed provides information on any of the routes in routes_list"
        return any(route in self.routes for route in routes_list)

    @staticmethod
    def feed_message() -> gtfs_realtime_pb2.FeedMessage:
        return gtfs_realtime_pb2.FeedMessage()
