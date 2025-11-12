import pandas as pd
import folium

def populate_map_with_stations(map: folium.Map, stations_df:pd.DataFrame) -> folium.Map:
    '''
    Create circle markers on the city map where the bike stations are.

    Args:
        map: A map in which to add markers
        stations_df: A dataframe with names and locations of stations. Following columns must be present:
            [lat, lng, name]

    Returns: map with added Circles

    TODO: branch where the station size depends on a certain metrics, such as number of bike changes
    '''

    for ix in range(stations_df.shape[0]):
        folium.Circle(location = (stations_df["lat"].iloc[ix], stations_df["lng"].iloc[ix]),
            tooltip = stations_df["name"].iloc[ix],
            radius = 5,
            fill = True,
            weight = 3,
            opacity = 0.6,
            color = "#0A3005"
        ).add_to(map)


    return map