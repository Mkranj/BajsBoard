import pandas as pd
import folium

def populate_map_with_stations(map: folium.Map,
    stations_df:pd.DataFrame,
    metric_size: str|None = None, 
    metric_tooltip_name: str|None = None) -> folium.Map:
    '''
    Create circle markers on the city map where the bike stations are.

    Args:
        map: A map in which to add markers
        stations_df: A dataframe with names and locations of stations. Following columns must be present:
            [lat, lng, name]
        metric_size: string, which column to use for calculating circle size? If None, all circles will have an uniform size.
        metric_tooltip_name: string, text to display before `metric_size` value. Must be provided if `metric_size` isn't None.

    Returns: map with added Circles

    '''
    if metric_size is not None:
        binned_metric = pd.qcut(stations_df[metric_size], 10, list(range(1, 10 + 1)))
        binned_metric = binned_metric.astype("float")

    for ix in range(stations_df.shape[0]):

        if metric_size is not None:
            tooltip_text = stations_df["name"].iloc[ix] + "<br>" + metric_tooltip_name + str(stations_df[metric_size].iloc[ix])
            # Radius depends on the metric
            custom_radius = binned_metric.iloc[ix] * 5
        else:
            tooltip_text = stations_df["name"].iloc[ix]
            custom_radius = 5

        folium.Circle(location = (stations_df["lat"].iloc[ix], stations_df["lng"].iloc[ix]),
            tooltip = tooltip_text,
            radius = custom_radius,
            fill = True,
            weight = 3,
            opacity = 0.6,
            color = "#0A3005"
        ).add_to(map)


    return map