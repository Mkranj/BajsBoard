# Functions for working with raw JSON data and transforming it to formats easier to use in further analysis

import json
import pandas as pd
import numpy as np
from datetime import datetime

def load_json(filename: str) -> dict:
    '''
    Shorthand for loading json from a file.

    Args:
        filename: JSON file location.

    Returns: dict, parsed JSON
    '''
    with open(filename) as json_data:
        parsed = json.load(json_data)
        json_data.close()
    return parsed


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

def calculate_bike_changes(earlier_bikes: pd.Series, later_bikes: pd.Series) -> pd.Series:
    '''
    Calculate how many bikes changed between two timepoints

    For each point we require a series of lists of bike IDs. 
    If a bike was present and then left we count that as a change. The same if a bike is now present that wasn't there before.
    These changes will serve as a measure of a stop's activity.
    
    Args:
        earlier_bikes: a series containing lists of integers, bike IDs
        later_bikes: a series containing lists of integers, bike IDs

    Returns: series of integers, number of changes between two time points
    '''
    changes = []
    no_changes = earlier_bikes.size

    for ix in range(no_changes):
        # earliest info will have no "bikes at station previously" so changes can't be calculated
        if (earlier_bikes[ix] is np.nan or
            later_bikes[ix] is np.nan):
            changes.append(np.nan)
            continue
        
        changed_ids  = list(set(earlier_bikes[ix]) ^ set(later_bikes[ix]))
        changes.append(len(changed_ids))

    return pd.Series(changes)