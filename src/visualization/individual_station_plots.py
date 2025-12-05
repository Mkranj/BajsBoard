from typing import Optional
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.figure import Figure

import base64
from io import BytesIO

def plot_hourly_changes_bar(station_data: pd.DataFrame, changes_type: str, ax: Optional[Axes] = None) -> Axes:
    '''
    Create a bar chart with average hourly changes.

    Changes type "out" plots only outgoing changes, while type "in/out" creates a stacked bar chart with
    incoming changes stacked on top of outgoing.

    The station_data should either be filtered to a single station, or aggregated for all stations total.

    Args:
        station_data: a dataframe grouped by hour (with hours as index)
        changes_type: ["out", "in/out"]. Whether to plot only outgoing or outgoing and incoming changes.
        ax: Optional Axes object. If provided, the plot will be added to that specific ax, allowing multiple axes to be combined in a single figure.

    Returns: Axes object with bar chart information.
    '''
    if ax is None:
        fig, ax = plt.subplots()
    
    if changes_type == "out":
        columns = ["outgoing"]
        stack = False
    elif changes_type == "in/out":
        columns = ["outgoing", "incoming"]
        stack = True

    station_data.plot(kind = "bar",
        y = columns, 
        stacked = stack, 
        legend = "reverse",
        ax=ax)

    ax.tick_params(axis = "x", labelrotation=0, labelsize=7)
    ax.set_xlabel(None)
    ax.set_ylabel("Prosječan broj uporaba u satu")
    
    if changes_type == "out":
        ax.get_legend().remove()
    elif changes_type == "in/out":
        ax.legend(labels = ["Odlazni", "Dolazni"])


    return ax

def plot_weekday_bar(station_data: pd.DataFrame, ax: Optional[Axes] = None) -> Axes:
    '''
    Create a bar chart with average changes for each weekday.

    The station_data should either be filtered to a single station, or aggregated for all stations total.

    Args:
        station_data: a dataframe grouped by wday (0-6, as index)
        ax: Optional Axes object. If provided, the plot will be added to that specific ax, allowing multiple axes to be combined in a single figure.

    Returns: Axes object with bar chart information.
    '''
    if ax is None:
        fig, ax = plt.subplots()

    columns = ["outgoing"]
    
    station_data.plot(kind = "bar",
        y = columns, 
        stacked = False,
        legend = False,
        ax = ax)

    ax.tick_params(axis = "x", labelrotation=0, labelsize=7)
    ax.set_xticklabels(["ponedjeljak", "utorak", "srijeda", "četvrtak", "petak", "subota", "nedjelja"])
    ax.set_xlabel(None)
    ax.set_ylabel("Prosječan broj uporaba u danu")

    return ax

def combined_plot_daily_weekly(station_data_hourly: pd.DataFrame, station_data_daily: pd.DataFrame) -> tuple[Figure, Axes]:
    '''
    Create a chart with hourly barchart on the left and weekday bar chart on the right.

    The hourly bar chart is stacked, with outgoing changes on the bottom and incoming on top.
    The station_data should either be filtered to a single station, or aggregated for all stations total.

    Args:
        station_data_hourly: a dataframe grouped by hour (with hours as index)
        station_data_daily: a dataframe grouped by wday (0-6, as index)
        
    Returns: (Figure, Axes) tuple. The figure is the combined chart.
    '''
    fig, ax = plt.subplots(nrows = 1, ncols = 2, figsize = (12, 4))

    _ = plot_hourly_changes_bar(station_data_hourly, changes_type = "in/out", ax = ax[0])
    _ = plot_weekday_bar(station_data_daily, ax = ax[1])
    
    plt.close(fig)
    return (fig, ax)

def stringify_plot(plot: Axes) -> str: 
    '''
    Turn a plot into a <img> tag with the base64-encoded string representation of the plot.

    Args:
        plot: Axes of a chart to be stringified.
        
    Returns: a string containing a <img> HTML tag, to be used as popup content.
    '''
    buf = BytesIO()
    plot.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)
    encoded = base64.b64encode(buf.read()).decode("utf-8")

    # HTML popup content
    html = f"""
    <img src="data:image/png;base64,{encoded}">
    """

    return html

def station_population_boxplots(population_df: pd.DataFrame, locations_df: pd.DataFrame, station_uids: list) -> Axes:
    plot_data = population_df[population_df["uid"].isin(station_uids)].merge(locations_df, on = "uid")

    # proporcije u postotke
    plot_data["population_prop"] *= 100
    
    # imena stanica - po dobivenom redoslijedu
    order_names = locations_df[locations_df["uid"].isin(station_uids)]
    order_names = order_names.set_index("uid").reindex(station_uids)["name"].to_list()

    ax = sns.boxplot(data = plot_data, y = "population_prop", x = "name", order = order_names)

    # referentne crte za 0% i 100%
    ax.axhline(0, ls="--", alpha = 0.3)
    ax.axhline(100, ls="--", alpha = 0.3)

    return ax