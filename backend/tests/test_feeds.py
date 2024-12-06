from unittest.mock import patch

from app.models import Feed
from app.service import Feeds

@patch("app.service.feeds.ENDPOINT_ROUTE_DICT", {
        "test-url-ACE": ["A", "C", "E"],
        "test-url-BDFM": ["B", "D", "F", "M"]
    })
def test_feeds():
    feeds = Feeds()
    assert len(feeds.feeds) == 2
    assert isinstance(feeds.feeds[0], Feed)
    assert feeds.feeds[0].endpoint_url == 'test-url-ACE'
    assert feeds.feeds[0].routes == ["A", "C", "E"]
