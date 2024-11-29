import pytest
from unittest.mock import AsyncMock, MagicMock, mock_open, patch

import httpx

from app.service import Feeds, StopTimes, SubwaySystem
from app.models import Stop, Route, Feed

def test_load_metadata():
    subway_system = SubwaySystem("tests/test-subway-stations.csv")
    assert len(subway_system.stops) == 2
    assert 'A1' in subway_system.stops
    assert 'B2' in subway_system.stops
    assert subway_system.stops['A1'].stop_name == "Test Stop"
    assert subway_system.stops['B2'].routes == ["B"]

    assert len(subway_system.routes["A"].stops) == 1
    assert len(subway_system.routes["B"].stops) == 1
    assert len(subway_system.routes["C"].stops) == 1
    assert subway_system.routes["D"].stops == []
    assert isinstance(subway_system.routes, dict)
    assert isinstance(subway_system.routes["A"], Route)

def test_missing_columns():
    mock_invalid_csv = """
    GTFS Stop ID,Stop Name,Daytime Routes
    A1,Test Stop,A C
    B2,Another Stop,B
    """
    with patch("builtins.open", mock_open(read_data=mock_invalid_csv)):
        with pytest.raises(KeyError):
            SubwaySystem(stations_path="dummy_path.csv")

def test_create_stop():
    stop_info = {
        "GTFS Stop ID": "123",
        "Stop Name": "Test Stop",
        "Daytime Routes": "A B",
        "North Direction Label": "Uptown",
        "South Direction Label": "Downtown",
    }

    stop = SubwaySystem.create_stop(stop_info)
    assert stop.gtfs_stop_id == "123"
    assert stop.stop_name == "Test Stop"
    assert stop.routes == ["A", "B"]
    assert stop.north_direction_label == "Uptown"
    assert stop.south_direction_label == "Downtown"
    assert isinstance(stop, Stop)

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


@pytest.mark.asyncio
@patch("app.service.stop_times.MessageToDict")
async def test_request_feed_success(mock_message_to_dict):
    # Mock httpx.AsyncClient.get
    mock_client = AsyncMock()
    mock_response = AsyncMock(status_code=200, content=b"mocked protobuf data")
    mock_client.get.return_value = mock_response

    # Mock feed and its feed_message method
    mock_feed = MagicMock(endpoint_url="https://mocked-feed-url.com")
    mock_feed_message = MagicMock()
    mock_feed.feed_message.return_value = mock_feed_message
    mock_feed_message.ParseFromString = MagicMock()

    # Mock MessageToDict to return a parsed protobuf message
    mock_message_to_dict.return_value = {"entity": []}

    # Call the method
    stop_times = StopTimes()
    result = await stop_times.request_feed(feed=mock_feed, client=mock_client)

    # Assertions
    mock_client.get.assert_awaited_once_with("https://mocked-feed-url.com")
    mock_feed_message.ParseFromString.assert_called_once_with(b"mocked protobuf data")
    assert result == {"entity": []}


@pytest.mark.asyncio
async def test_request_feed_error():
    mock_client = AsyncMock()
    mock_client.get.side_effect = httpx.HTTPError("Error")

    mock_feed = MagicMock(endpoint_url="https://mocked-feed-url.com")
    stop_times = StopTimes()

    with pytest.raises(Exception, match="error retrieving data from endpoint"):
        await stop_times.request_feed(feed=mock_feed, client=mock_client)