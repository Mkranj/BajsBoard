import folium

def populate_map_with_stations(map, stations_df):
    '''
    Create circle markers on the city map where the bike stations are.

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