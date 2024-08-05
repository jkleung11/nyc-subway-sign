import csv
from typing import Dict, List, Tuple

from pydantic import BaseModel

from app.models.stop import Stop
from app.models.route import Route
from metadata.constants import ROUTE_ENDPOINT_DICT


class SubwaySystem(BaseModel):
    """
    parses stations file to represent the subway system

    stops_map: dict of stop_id: Stop
    routes: dict of route_name: Route?
    """

    stations_path: str
    routes: Dict[str, Route] = None

    def model_post_init(self, __context) -> None:
        self.routes = self.load_routes()

    def load_routes(self):
        routes = {route_name: [] for route_name in ROUTE_ENDPOINT_DICT.keys()}

        with open(self.stations_path, "r") as stations_file:
            reader = csv.DictReader(stations_file)
            for stop_info in reader:
                stop = self.create_stop(stop_info=stop_info)
                for route_name in stop.routes:
                    if route_name in ROUTE_ENDPOINT_DICT.keys():
                        routes[route_name].append(stop)

        # first character in gtfs stop id signifies route id
        # subsequent characters increase as train moves south
        return {
            route_name: Route(name=route_name, stops=stops)
            for route_name, stops in routes.items()
        }

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
