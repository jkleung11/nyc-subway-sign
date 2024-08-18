from typing import List, Dict

from metadata.constants import ENDPOINT_ROUTE_DICT
from app.models.feed import Feed
from app.models.stop import Stop


class Feeds():
    
    def __init__(self, endpoint_route_dict: Dict):
        self.feeds = self.load_feeds(endpoint_route_dict)
    
    @staticmethod
    def load_feeds(endpoint_route_dict: Dict):
        return [Feed(endpoint_url=url) for url in endpoint_route_dict.keys()]
    
    def feeds_for_stop(self, stop: Stop) -> List[Feed]:
        feeds = []
        for feed in self.feeds: 
            if feed.has_routes(stop.routes):
                feeds.append(feed)
        return feeds