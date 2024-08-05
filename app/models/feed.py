from typing import List

import requests
from pydantic import BaseModel, field_validator
from google.transit import gtfs_realtime_pb2

from metadata.constants import ENDPOINT_ROUTE_DICT


class Feed(BaseModel):
    """
    wrapper for FeedMessage protocol, includes attributes for the endpoint
    and its corresponding routes
    """

    endpoint_url: str

    @property
    def routes_in_feed(self):
        return ENDPOINT_ROUTE_DICT[self.endpoint_url]

    @field_validator("endpoint_url")
    @classmethod
    def valid_url(cls, endpoint_url: str):
        assert endpoint_url in ENDPOINT_ROUTE_DICT
        return endpoint_url

    @staticmethod
    def feed_message() -> gtfs_realtime_pb2.FeedMessage:
        return gtfs_realtime_pb2.FeedMessage()
