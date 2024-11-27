import pytest
from unittest.mock import mock_open, patch, MagicMock
from app.service import SubwaySystem
from app.models import Stop, Route

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
