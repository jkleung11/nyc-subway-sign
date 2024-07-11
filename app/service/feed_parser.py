from typing import Dict

from google.transit import gtfs_realtime_pb2
from google.protobuf_json_format import MessageToDict
from pydantic import BaseModel
import requests

from app.models.feed import Feed

class FeedParser(BaseModel):

    def get_feed_json(self, feed: Feed) -> Dict:
        try: 
            resp = requests.get(feed.endpoint_url)
            resp.raise_for_status()
        except requests.exceptions.RequestException as e:
            raise Exception(f"error retrieving data from endpoint {feed.endpoint_url}": {e})
        
        feed_message = feed.message()
        feed_message.ParseFromString(resp.content)
        return MessageToDict(feed_message)