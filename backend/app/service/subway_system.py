import csv
from typing import Tuple, Dict


from app.models import Route, Stop
from metadata.constants import ROUTE_ENDPOINT_DICT


class SubwaySystem:
    """
    parses stations file to represent the subway system

    stations_path: filepath to read on start up
    routes: dict of route_id: Route
    stops: dict of gtfs_stop_id: Stop
    """

    def __init__(self, stations_path: str):
        self.stations_path = stations_path
        self.routes, self.stops = self.load_metatdata()

    def load_metatdata(self) -> Tuple[Dict, Dict]:
        routes = {route_name: [] for route_name in ROUTE_ENDPOINT_DICT.keys()}
        stops = {}

        with open(self.stations_path, "r") as stations_file:
            reader = csv.DictReader(stations_file)
            for stop_info in reader:
                stop = self.create_stop(stop_info=stop_info)
                for route_name in stop.routes:
                    if route_name in ROUTE_ENDPOINT_DICT.keys():
                        routes[route_name].append(stop)
                stops[stop.gtfs_stop_id] = stop

        # first character in gtfs stop id signifies route id
        # subsequent characters increase as train moves south
        routes = {
            route_name: Route(name=route_name, stops=stops_list)
            for route_name, stops_list in routes.items()
        }
        return routes, stops

    @staticmethod
    def create_stop(stop_info: Dict) -> Stop:
        """return instance of a Stop class"""
        stop_info_keys = [
            "GTFS Stop ID",
            "Stop Name",
            "Daytime Routes",
            "North Direction Label",
            "South Direction Label",
        ]
        kwargs = {
            key.lower().replace(" ", "_"): stop_info[key] for key in stop_info_keys
        }
        kwargs["routes"] = kwargs.pop("daytime_routes").split(" ")
        return Stop(**kwargs)
