import csv
from typing import Dict, List

from pydantic import BaseModel

from app.models.stop import Stop
from metadata.constants import ROUTE_ENDPOINT_DICT


class SubwaySystem(BaseModel):
    """parses stations file to create a dict of stop_id: Stop"""

    stations_path: str
    system_map: Dict = None

    def model_post_init(self, __context) -> None:
        self.system_map = self.load_system_map()

    @property
    def system_routes(self) -> List[str]:
        return list(ROUTE_ENDPOINT_DICT.keys())

    def load_system_map(self):
        """create the system map of stop_id: Stop()"""

        system_map = {}
        with open(self.stations_path, "r") as stations_file:
            reader = csv.DictReader(stations_file)
            for stop_info in reader:
                stop_id = stop_info["GTFS Stop ID"]
                system_map[stop_id] = self.load_stop(stop_info)
        return system_map

    def load_stop(self, stop_info: Dict) -> Stop:
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

    def stops_on_route(self, route: str) -> List[Dict]:
        if route not in self.system_routes:
            raise ValueError(
                f"invalid route option, choose one of {self.system_routes}"
            )
        stops_on_route = [
            {
                "name": stop.stop_name,
                "routes": stop.routes,
                "gtfs-stop-id": stop.gtfs_stop_id,
            }
            for stop in self.system_map.values()
            if route in stop.routes
        ]
        return stops_on_route