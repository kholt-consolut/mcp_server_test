from mcp.server.fastmcp import FastMCP
from datetime import datetime
import requests
import json

import pandas as pd
import shapely
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon



service_url_station = "https://app-prod-ws.warnwetter.de/v30/stationOverviewExtended"
service_url_location = "https://s3.eu-central-1.amazonaws.com/app-prod-static.warnwetter.de/v16/gemeinde_warnings_v2.json"



# Create an instance of the FastMCP server
mcp = FastMCP("WeatherWarnings", stateless_http=True)

@mcp.tool(description="Provides the DWD weather warnings for a station given by its ID")
def get_weather_warnings_station(station_id: str) -> str:
    """
    Use this tool to get the weather warnings for a station with given ID.

    The warnings are retrieved from the Deutsche Wetterdienst (DWD).

    Args:
        station_id: The ID of the station

    Returns:
    str: The warnings as a JSON string.
    """
    params={"stationIds": [station_id]}
    response = requests.get(service_url_station, headers={"Accept": "application/json"}, verify=False, params=params)
    return json.dumps(response.json()[station_id]["warnings"])


@mcp.tool(description="Provides the DWD weather warnings for a location given by latitude and longitude")
def get_weather_warnings_location(lat: float, lon: float) -> str:
    """
    Use this tool to get the weather warnings for a location given by latitude and longitude.

    The warnings are retrieved from the Deutsche Wetterdienst (DWD).

    Args:
        lat: The latitude of the location
        lon: The longitude of the location

    Returns:
    list[str]: The warnings as a JSON string.
    """
    response = requests.get(service_url_location, verify=False, headers={"Accept": "application/json"})

    df = pd.DataFrame(response.json()["warnings"])

    point = Point([lon , lat])

    warnings = []

    for index, line in df.iterrows():

        polygons = []
        for item in line["regions"]:
            polygons.append(Polygon(item["polygonGeometry"]["coordinates"][0]))
        great_polygon = shapely.coverage_union_all(polygons)
        if great_polygon.contains(point):
            warnings.append(line[["level", "headLine", "description", "instruction"]].to_dict())
    
    return json.dumps(warnings)