import time
from unittest.mock import AsyncMock, MagicMock, patch

import httpx
import pytest

from app.models import Arrival, TimesRequest
from app.service import StopTimes

@pytest.mark.asyncio
@patch("app.service.stop_times.StopTimes.request_feed", new_callable=AsyncMock)
@patch("app.service.stop_times.StopTimes.parse_feed_message")
async def test_get_arrivals(mock_parse, mock_request):
    mock_stop = MagicMock()
    mock_feed = MagicMock()
    mock_client= MagicMock()
    stop_times = StopTimes()

    await stop_times.get_arrivals(mock_stop, mock_feed, mock_client)
    mock_request.assert_awaited_once_with(feed=mock_feed, client=mock_client)
    mock_parse.assert_called_once_with(feed_message=mock_request.return_value, stop=mock_stop)

@patch("app.service.stop_times.StopTimes.parse_arrival")
def test_parse_feed_message(mock_parse_arrival):
    mock_stop_time_updates = MagicMock()
    mock_stop = MagicMock()
    feed_message = {
        "entity": [
            {
                "no_trip_update": ""
            },
            {
                "tripUpdate": {
                    "no_stop_time_update": ""
                }
            },
            {
                "tripUpdate": {
                    "stopTimeUpdate": mock_stop_time_updates,
                    "trip": {
                        "routeId": "A"
                    }
                }
            }
        ]
    }
    stop_times = StopTimes()
    parsed_message = stop_times.parse_feed_message(feed_message, mock_stop)
    assert isinstance(parsed_message, list)
    mock_parse_arrival.assert_called_once_with(mock_stop_time_updates, mock_stop, "A")



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