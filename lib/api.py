import os
from datetime import timedelta
import pandas as pd
data = {}

def read_co2_weekly(filepath):
    df = pd.read_csv(filepath)
    df["date"] = pd.to_datetime(df[["year", "month", "day"]])
    df = df.reindex(['date','ppm', '1 yr ago.', '10 yr ago','since 1800', '# days', 'year', 'month', 'day', 'decimal'], axis=1)
    df.sort_values(by="date", inplace=True)
    return df

def load(path):
    resolved_filepath = lambda f: os.path.join(path, f)
    data["co2_weekly"] = read_co2_weekly(resolved_filepath("co2_weekly_mlo-2.csv"))

def ppm_at(date):
    df = data["co2_weekly"]
    searched = pd.to_datetime(date)
    lower_bound = searched - timedelta(days=14)
    upper_bound = searched + timedelta(days=14)
    return df[(df["date"] < upper_bound) & (df["date"] > lower_bound)] 

def ppm_yearly_average():
    df = data["co2_weekly"]
    return pd.DataFrame(df.groupby("year", as_index=False)["ppm"].mean())

def ppm_monthly_average():
    df = data["co2_weekly"]
    return pd.DataFrame(df.groupby(by=["year", "month"], as_index=False)["ppm"].mean())

def ppm_biweekly_average():
    df = data["co2_weekly"]
    return df[["year", "month", "day", "ppm"]]
