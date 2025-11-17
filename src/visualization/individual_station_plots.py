from typing import Optional
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.axes import Axes

import base64
from io import BytesIO

def plot_hourly_bar(station_data: pd.DataFrame, changes_type: str, ax: Optional[Axes] = None) -> Axes:
    if ax is None:
        fig, ax = plt.subplots()
    
    if changes_type == "total":
        columns = ["changes"]
        stack = False
    elif changes_type == "in/out":
        columns = ["incoming", "outgoing"]
        stack = True

    station_data.plot(kind = "bar",
        y = columns, 
        stacked = stack, 
        legend = "reverse",
        ax=ax)

    ax.tick_params(axis = "x", labelrotation=0)

    return ax

def plot_weekday_bar(station_data: pd.DataFrame, ax: Optional[Axes] = None) -> Axes:
    if ax is None:
        fig, ax = plt.subplots()

    columns = ["changes"]
    
    station_data.plot(kind = "bar",
        y = columns, 
        stacked = False,
        legend = False,
        ax = ax)

    ax.tick_params(axis = "x", labelrotation=0)
    ax.set_xticklabels(["ponedjeljak", "utorak", "srijeda", "četvrtak", "petak", "subota", "nedjelja"])
    ax.set_xlabel(None)

    return ax

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