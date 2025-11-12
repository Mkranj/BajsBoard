# Functions for working with raw JSON data and transforming it to formats easier to use in further analysis

import pandas as pd

def trim_json_to_locations(json):
    '''
    Extract the locations array from the raw scraped JSON

    Information higher in the hierarchy is unchanging, so we don't need to worry about it in individual files.
    '''
    return json["countries"][0]["cities"][0]["places"]

def gather_bajs_locations(loc_list):
    '''
    Create a dataframe of all available locations
    
    Takes a list of full location data from `trim_json_to_locations`.
    Under assumption that Bajs locations don't change. If they do, possible upgrade is to take an overlap of multiple such calls. 
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