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

def calculate_bike_changes(earlier_bikes: pd.Series, later_bikes: pd.Series) -> dict[pd.Series]:
    '''
    Calculate how many bikes changed between two timepoints

    For each point we require a series of lists of bike IDs. 
    If a bike was present and then left we count that as a change. The same if a bike is now present that wasn't there before.
    These changes will serve as a measure of a stop's activity.
    
    Args:
        earlier_bikes: a series containing lists of integers, bike IDs
        later_bikes: a series containing lists of integers, bike IDs

    Returns: dictionary {changes, incoming, outgoing}. Each a Series of integers, number of such changes between two time points. "Changes" is combined both incoming and outgoing.
    '''
    changes = []
    no_changes = earlier_bikes.size

    incoming = []
    outgoing = []

    for ix in range(no_changes):
        earlier_ids = earlier_bikes[ix]
        later_ids = later_bikes[ix]

        # earliest info will have no "bikes at station previously" so changes can't be calculated
        if (earlier_ids is np.nan or
            later_ids is np.nan):
            changes.append(np.nan)
            incoming.append(np.nan)
            outgoing.append(np.nan)
            continue
        
        # General changes - any bikes that arrived or left location
        changed_ids  = list(set(earlier_ids) ^ set(later_ids))
        changes.append(len(changed_ids))

        is_incoming = [bike not in earlier_ids for bike in later_ids]
        incoming.append(sum(is_incoming))

        is_outgoing = [bike not in later_ids for bike in earlier_ids]
        outgoing.append(sum(is_outgoing))

    return {
        "changes": pd.Series(changes),
        "incoming": pd.Series(incoming),
        "outgoing": pd.Series(outgoing)
    }

def create_changes_columns(location_bikes: pd.DataFrame) -> pd.DataFrame:
    #TODO DESCRIPTION

    # Sorting to ensure lags refer to exactly the first earlier observed time
    df = location_bikes.sort_values(["time", "uid"])

    df["lag1_time"] = df.groupby(["uid"])["time"].shift(1)

    df = (
        df.merge(
            df.drop(["lag1_time"], axis = 1), # so we don't get this as an additional column after join
            how = "left",
            left_on = ["uid", "lag1_time"],
            right_on = ["uid", "time"],
            suffixes = (None, "_lag1")
            )
            .drop(
                ["time_lag1"], axis = 1
            )
        )

    changes = calculate_bike_changes(
        df["bikes_at_station_lag1"],
        df["bikes_at_station"]
        )

    df["changes"] = changes["changes"]
    df["incoming"] = changes["incoming"]
    df["outgoing"] = changes["outgoing"]

    return df