# Functions for working with raw JSON data and transforming it to formats easier to use in further analysis

import pandas as pd
from datetime import datetime

def trim_json_to_locations(json: dict) -> list:
    '''
    Extract the locations array from the raw scraped JSON

    Information higher in the hierarchy is unchanging, so we don't need to worry about it in individual files.

    Args:
        json: a dict made from parsed raw JSON obtained by scraping.

    Returns: list of dicts, each a Bajs location
    '''
    return json["countries"][0]["cities"][0]["places"]

def gather_bajs_locations(loc_list: list[dict]) -> pd.DataFrame:
    '''
    Create a dataframe of all available locations
    
    Takes a list of full location data from `trim_json_to_locations`.
    Under assumption that Bajs locations don't change. If they do, possible upgrade is to take an overlap of multiple such calls. 
    
    Args:
        loc_list: A list of Bajs racks locations, each a dict with name, location, bike info etc.

    Returns: dataframe with each row being a Bajs location
    '''

    loc_uid = [loc["uid"] for loc in loc_list]
    loc_name = [loc["name"] for loc in loc_list]
    loc_lat = [loc["lat"] for loc in loc_list]
    loc_lng = [loc["lng"] for loc in loc_list]
    loc_racks = [loc["bike_racks"] for loc in loc_list]

    df = pd.DataFrame({
        "uid": loc_uid,
        "name": loc_name,
        "lat": loc_lat,
        "lng": loc_lng,
        "no_racks": loc_racks
    })

    return df

def get_bikes_in_stations(time: datetime, loc_list: list[dict]) -> pd.DataFrame:
    '''
    Create a dataframe of bike IDS at a certain station at a certain time
    
    Takes a list of full location data from `trim_json_to_locations`.
    Each row has the datetime info, so multiple such df's can be combined while retaining all relevant information.
    
    Args:
        time: datetime describing when the info was gathered
        loc_list: A list of Bajs racks locations, each a dict with name, location, bike info etc.

    Returns: dataframe each row being a Bajs location (identified by uid) at a certain time, with list of individual bike IDs at that station
    '''

    locations = []
    bike_ids = []

    for location in loc_list:
        locations.append(location["uid"])
        bike_ids.append(location["bike_numbers"])

    df = pd.DataFrame({
        "uid": locations,
        "time": time, # same for all rows
        "bikes_at_station": bike_ids
    })

    return df