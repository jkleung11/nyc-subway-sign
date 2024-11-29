import pytest
from unittest.mock import MagicMock, mock_open, patch
from app.service import Feeds, SubwaySystem
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