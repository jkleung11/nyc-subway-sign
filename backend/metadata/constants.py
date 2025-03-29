ENDPOINT_ROUTE_DICT = {
    "https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-ace": [
        "A",
        "C",
        "E",
    ],
    "https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-bdfm": [
        "B",
        "D",
        "F",
        "M",
    ],
    "https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-g": ["G"],
    "https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-jz": ["J", "Z"],
    "https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-l": ["L"],
    "https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-nqrw": [
        "N",
        "Q",
        "R",
        "W",
    ],
    "https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs": [
        "1",
        "2",
        "3",
        "4",
        "5",
        "6",
        "7",
        "S"
    ],
}

ROUTE_ENDPOINT_DICT = {
    route: url for url, routes in ENDPOINT_ROUTE_DICT.items() for route in routes
}
