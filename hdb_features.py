"""Shared feature engineering for the HDB resale price predictor.

Both model.py (training) and app.py (serving) import from this file, so the
model always receives features built in exactly the same way. Training and
serving code drifting apart is one of the most common bugs in deployed ML.
"""

from pathlib import Path

import pandas as pd

DATA_PATH = Path(__file__).parent / "data" / "hdb_resale_2017_2019.csv"

# Original source of the CSV (a mirror of data.gov.sg, Jan 2017 - May 2019).
# A local copy is kept in data/ so the lesson still works if this link breaks.
DATA_URL = (
    "https://raw.githubusercontent.com/kohjiaxuan/"
    "Predicting-HDB-Price-with-Machine-Learning/master/"
    "resale-flat-prices-based-on-registration-date-from-jan-2017-onwards.csv"
)

CATEGORICAL_FEATURES = ["town", "flat_type"]
NUMERIC_FEATURES = ["floor_area_sqm", "storey", "lease_commence_date"]
FEATURES = CATEGORICAL_FEATURES + NUMERIC_FEATURES
TARGET = "resale_price"


def load_data(path=DATA_PATH):
    """Load the resale CSV from the local copy, falling back to the URL."""
    if Path(path).exists():
        return pd.read_csv(path)
    return pd.read_csv(DATA_URL)


def storey_midpoint(storey_range):
    """Turn a storey band such as '10 TO 12' into its midpoint (11.0)."""
    bounds = storey_range.str.split(" TO ", expand=True).astype(int)
    return (bounds[0] + bounds[1]) / 2


def add_features(df):
    """Return a copy of the raw data with the engineered 'storey' column."""
    df = df.copy()
    df["storey"] = storey_midpoint(df["storey_range"])
    return df
