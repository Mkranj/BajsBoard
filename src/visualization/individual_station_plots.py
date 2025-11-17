import pandas as pd
import seaborn as sns
import matplotlib as plt

def plot_hourly_bar(station_data: pd.DataFrame, changes_type: str):
    if changes_type == "total":
        columns = ["changes"]
        stack = False
    elif changes_type == "in/out":
        columns = ["incoming", "outgoing"]
        stack = True

    chart = station_data.plot(kind = "bar",
        y = columns, 
        stacked = stack, 
        legend = "reverse")

    chart.tick_params(axis = "x", labelrotation=0)

    return chart

def plot_weekday_bar(station_data: pd.DataFrame, changes_type: str):
    # TODO - without in out?
    if changes_type == "total":
        columns = ["changes"]
        stack = False
    elif changes_type == "in/out":
        columns = ["incoming", "outgoing"]
        stack = True

    chart = station_data.plot(kind = "bar",
        y = columns, 
        stacked = stack, 
        legend = "reverse")

    chart.tick_params(axis = "x", labelrotation=0)

    return chart