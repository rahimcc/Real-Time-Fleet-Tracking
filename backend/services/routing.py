
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
    

def geocode(place_name: str) -> tuple[float,float]: 
    """ 
    Converts name of location into geocoordinates 

        Args:
            place_name : Name of the place 
        
        Returns: 

            tuple[float,float]: Tuple of coordinates 

    """

    url = "https://nominatim.openstreetmap.org/search"
    params = {"q": place_name, "format": "json", "limit": 1 }
    headers = { "User-Agent": "fleet-tracking-demo/1.0"}


    try: 
        response = requests.get(url , params=params, headers=headers, timeout= 5)
        results = response.json()

        if not results: 
            return None

        lat = float(results[0]["lat"])
        lon = float(results[0]["lon"])

        return lat,lon 

    except Exception as e:

        print(f'geocode error: {e}')
        return None 


print ( geocode('Baku'))