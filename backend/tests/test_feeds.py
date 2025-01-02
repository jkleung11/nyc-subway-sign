from unittest.mock import patch

from app.models import Feed, Stop
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

def test_feeds_for_stop():
    feeds = Feeds()
    single_feed_stop = Stop(gtfs_stop_id="A1", stop_name="Single Feed", routes=["A", "C", "E"],
                            north_direction_label="Manhattan", south_direction_label="Brooklyn")
    multiple_feed_stop = Stop(gtfs_stop_id="A2", stop_name="Multi Feed", routes=["A", "D"],
                              north_direction_label="Manhattan", south_direction_label="Brooklyn")
    assert len(feeds.feeds_for_stop(single_feed_stop)) == 1
    assert len(feeds.feeds_for_stop(multiple_feed_stop)) == 2
