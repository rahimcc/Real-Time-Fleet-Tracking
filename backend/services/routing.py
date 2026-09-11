
"""
routing.py

Wraps OSRM's public routing API to convert start/end coordinate pair 
into a list of points tracing an actual road path.

Currently uses public OSRM demo server

"""

import requests


OSRM_URL = "http://router.project-osrm.org/route/v1/driving"



def fetch_route(start_lat, start_lon, end_lat, end_lon) -> list[tuple[float,float]]:
    """
    Returns a list of (lat,lon) points tracing real roads between 
    two coordinates, or an empty list if no route could be found.
    
    Args:
        start_lat , start_lon: starting coordinates
        end_lat, end_lon: destination coordinates

    Returns: 
        list[tuple[float,float]]: ordered (lat,lon) points along the route, or [] on failure.
    """

    url = f'{OSRM_URL}/{start_lon},{start_lat};{end_lon},{end_lat}'
    params = {"overview": "full", "geometries": "geojson"}


    try: 

        response = requests.get(url, params=params, timeout= 5)
        data = response.json()

        if data.get('code') != "Ok":
            return []

        coords = data['routes'][0]['geometry']['coordinates']

        return [ (lat,lon) for lat,lon in coords]
    except Exception as e:
        print(f'fetch_route error: {e}')

        return []
    

print(fetch_route(40.3777,49.8920,40.4093, 49.8671))