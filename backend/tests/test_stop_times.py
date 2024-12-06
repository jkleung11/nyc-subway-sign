import time
from unittest.mock import AsyncMock, MagicMock, patch

import httpx
import pytest

from app.models import Arrival, TimesRequest
from app.service import StopTimes

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

def test_filter_arrivals():
    first = {
        "route_id": "A",
        "gtfs_stop_id": "A1",
        "direction_label": "Manhattan",
        "direction_letter": "N",
        "arrival_time": str(int(time.time() + 120)),
        "arrival_mins": 2
    }
    second = {
        "route_id": "A",
        "gtfs_stop_id": "A1",
        "direction_label": "Manhattan",
        "direction_letter": "N",
        "arrival_time": str(int(time.time() + 900)),
        "arrival_mins": 15
    }
    arrivals = [
        Arrival(**first),
        Arrival(**second)
    ]
    
    stop_times = StopTimes()
    request = TimesRequest(gtfs_stop_id="A1", min_mins=0, max_mins=5)
    filtered = stop_times.filter_arrivals([arrivals], request)
    assert len(filtered) == 1
    assert filtered[0].arrival_mins == 2
    
    # no trains within our time
    request = TimesRequest(gtfs_stop_id="A1", min_mins=0, max_mins=1)
    filtered = stop_times.filter_arrivals([arrivals], request)
    assert filtered == []