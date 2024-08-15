import pandas as pd

from india_api.internal import PredictedPower



def format_csv(values: list[PredictedPower]) -> pd.DataFrame:
    """
    Format the predicted power values into a pandas dataframe ready for CSV export.

    The pandas dataframes ends up with
    - Date [IST]: The date
    - Time: start and end time, e.g 00:00 to 00:15
    - PowerKW, the forecasted power

    """
    # change list of prediction power to pandas dataframe
    df = pd.DataFrame([y.__dict__ for y in values])

    # change Time columns from UTC to IST
    df["Time"] = pd.to_datetime(df["Time"]).dt.tz_convert("Asia/Kolkata")

    # create date columns
    df["Date [IST]"] = df["Time"].dt.date
    # create start and end time column and only show HH:MM
    df["Start Time [IST]"] = df["Time"].dt.strftime("%H:%M")
    df["End Time [IST]"] = (df["Time"] + pd.to_timedelta("15T")).dt.strftime("%H:%M")

    # combine start and end times
    df["Time"] = df["Start Time [IST]"].astype(str) + " - " + df["End Time [IST]"].astype(str)

    # drop start and end columns and order
    df = df.drop(columns=["Start Time [IST]", "End Time [IST]"])
    df = df[["Date [IST]", "Time", "PowerKW"]]

    # only get tomorrows results. This is for IST time.
    now_ist = pd.Timestamp.now(tz="Asia/Kolkata")
    tomorrow = now_ist + pd.Timedelta(days=1)
    df = df[df["Date [IST]"] == tomorrow.date()]

    return df
