import pandas as pd
import seaborn as sns
import matplotlib as plt

import base64
from io import BytesIO

def plot_hourly_bar(station_data: pd.DataFrame, changes_type: str) -> plt.axes:
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

def plot_weekday_bar(station_data: pd.DataFrame) -> plt.axes:
    columns = ["changes"]
    
    chart = station_data.plot(kind = "bar",
        y = columns, 
        stacked = False,
        legend = False)

    chart.tick_params(axis = "x", labelrotation=0)
    chart.set_xticklabels(["ponedjeljak", "utorak", "srijeda", "četvrtak", "petak", "subota", "nedjelja"])
    chart.set_xlabel(None)

    return chart

def stringify_plot(plot: plt.axes):
    buf = BytesIO()
    plot.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)
    encoded = base64.b64encode(buf.read()).decode("utf-8")

    # HTML popup content
    html = f"""
    <img src="data:image/png;base64,{encoded}">
    """

    return html