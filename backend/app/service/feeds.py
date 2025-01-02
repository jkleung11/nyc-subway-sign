from typing import List, Dict

from app.models import Feed, Stop
from metadata.constants import ENDPOINT_ROUTE_DICT


class Feeds:
    """
    creates Feed objects by iterating through dict of endpoint urls and the associated routes
    """

    def __init__(self):
        self.feeds = self.load_feeds()

    @staticmethod
    def load_feeds():
        return [Feed(endpoint_url=url, routes=routes) for url, routes in ENDPOINT_ROUTE_DICT.items()]

    def feeds_for_stop(self, stop: Stop) -> List[Feed]:
        """
        Return a list of Feed objects that are needed to get times for a specific Stop
        """
        feeds = []
        for feed in self.feeds:
            if feed.has_routes(stop.routes):
                feeds.append(feed)
        return feeds
