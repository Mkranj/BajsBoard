import pandas as pd

def create_hourly_df(timepoints_df: pd.DataFrame) -> pd.DataFrame:
    df = timepoints_df
    df["hour"] = df["time"].dt.hour
    
    # If there is more than one row for a given station in a given hour, first sum to get totals for hour
    # THEN average across all available days
    df = df.groupby(["uid", "time", "hour"]).sum(["changes", "incoming", "outgoing"])

    df = df.groupby(["uid", "hour"]).mean(["changes", "incoming", "outgoing"])

    # Filling in potentially missing station/hour combination with 0 changes

    hours_index = pd.MultiIndex.from_product([timepoints_df["uid"].unique().tolist(),
        list(range(24))],
        names = ["uid", "hour"])
    
    df = df.reindex(hours_index, fill_value = 0)

    return df

def create_weekday_df(timepoints_df: pd.DataFrame) -> pd.DataFrame:
    df = timepoints_df

    # We need the precise day to group by to accumulate changes for each observed day,
    # only then can we "group up" by day of week
    df["date"] = df["time"].dt.date
    df["wday"] = df["time"].dt.weekday

    daily = df.groupby(["uid", "date"]).agg({
        "changes": "sum",
        "incoming": "sum",
        "outgoing": "sum",
        "wday": "first"
    })

    weekdaily = daily.groupby(["uid", "wday"]).mean(["changes", "incoming", "outgoing"])

    # Filling in missing station/weekday combination with 0 changes

    days_index = pd.MultiIndex.from_product([timepoints_df["uid"].unique().tolist(),
        list(range(7))],
        names = ["uid", "wday"])
    
    weekdaily = weekdaily.reindex(days_index, fill_value = 0)

    return weekdaily
