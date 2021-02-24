import os
from datetime import timedelta
import pandas as pd
data = {}

KEYS = [
    "mlo_weekly_co2.csv",
    # sourced from https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=1310039401
    "statcan_leading_cause_of_death.csv"
]

def load(path, key, force=False):
    if key not in data or force is True:
        fp = os.path.join(path, key)
        print(f"Loading {key}...")
        if key == "mlo_weekly_co2.csv":
            data[key] = read_mlo_weekly_co2_csv(fp)
        elif key == "statcan_leading_cause_of_death.csv":
            data[key] = pd.read_csv(fp)

def load_all(path):
    for k in KEYS:
        load(path, k, force=True)

# Decorator for preloading required data
def load_data(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

def read_mlo_weekly_co2_csv(filepath):
    df = pd.read_csv(filepath)
    df["date"] = pd.to_datetime(df[["year", "month", "day"]])
    df = df.reindex(['date','ppm', '1 yr ago.', '10 yr ago','since 1800', '# days', 'year', 'month', 'day', 'decimal'], axis=1)
    df.sort_values(by="date", inplace=True)
    return df

def ppm_at(date):
    df = data["mlo_weekly_co2.csv"]
    searched = pd.to_datetime(date)
    lower_bound = searched - timedelta(days=14)
    upper_bound = searched + timedelta(days=14)
    return df[(df["date"] < upper_bound) & (df["date"] > lower_bound)] 

def ppm_yearly_average():
    df = data["mlo_weekly_co2.csv"]
    return pd.DataFrame(df.groupby("year", as_index=False)["ppm"].mean())

def ppm_monthly_average():
    df = data["mlo_weekly_co2.csv"]
    return pd.DataFrame(df.groupby(by=["year", "month"], as_index=False)["ppm"].mean())

def ppm_biweekly_average():
    df = data["mlo_weekly_co2.csv"]
    return df[["year", "month", "day", "ppm"]]

def leading_cause_of_death_by_year(year):
    df = data["statcan_leading_cause_of_death.csv"]
    years_available = df["REF_DATE"].unique()
    assert year in years_available, f"File does not contain data for {year}, choose from {years_available}"
    df = df[(df["REF_DATE"] == 2015) & (df["Characteristics"] == "Number of deaths")]
    cols_to_keep = ["REF_DATE", "GEO", "Leading causes of death (ICD-10)", "VALUE"]
    return df[cols_to_keep].sort_values(by="VALUE", ascending=False)
