import os
from datetime import datetime, timedelta

import numpy as np
import pandas as pd
from dateutil import parser
from loguru import logger

from app import cache
from pages.drug_tracker.constants import ALCOHOL_DICT, DATABASE_ID
from tools.notion import get_database

logger.add(
    os.path.join(os.path.dirname(os.path.abspath(__file__)) + "/logs/" + os.path.basename(__file__) + ".log"),
    format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}",
    backtrace=True,
    diagnose=True,
)


def get_names(row):
    temp_list = []
    for entry in row:
        temp_list.append(entry["name"])
    return " | ".join(temp_list)


def calculate_alcohol_density(row):
    drinks = row.split("|")
    if len(drinks) > 0 and drinks[0]:
        alcohol_in_gram = []
        all_gram = 0.0

        for drink in drinks:
            count = [int(s) for s in drink.split() if s.isdigit()][0]
            name_of_drink = "".join([i for i in drink if not i.isdigit()]).strip()
            name_of_drink = "".join([i for i in name_of_drink if i.isalnum()]).strip()
            gram = ALCOHOL_DICT[name_of_drink]
            entry = {"count": count, "name": name_of_drink, "gram": gram}
            alcohol_in_gram.append(entry)
            all_gram = all_gram + count * gram
        return all_gram


def calculate_nicotine_density(row):
    if row:
        if "Snus Pouch" in row:
            return 1
        if row[0] == ">":
            count = 0.5
            row = row[4:]
        else:
            count = int(row[0])
            row = row[1:]
        people_count = int("".join([i for i in row if i.isdigit()]).strip())
        return count / people_count


def initial_clean(df):
    df = df[
        [
            "properties~Date~date~start",
            "properties~Alcohol~multi_select",
            "properties~Nicotine~multi_select",
        ]
    ]
    df["properties~Date~date~start"] = df["properties~Date~date~start"].apply(lambda row: parser.parse(row))
    df = df[df["properties~Date~date~start"] <= (datetime.now() - timedelta(days=1))]
    df.sort_values("properties~Date~date~start", inplace=True)

    df["Date"] = df["properties~Date~date~start"]
    df.drop("properties~Date~date~start", axis=1, inplace=True)
    df["Date"] = pd.to_datetime(df["Date"])
    df["Alcohol"] = df["properties~Alcohol~multi_select"].apply(lambda row: get_names(row))
    df.drop("properties~Alcohol~multi_select", axis=1, inplace=True)
    df["Alcohol-Intake"] = df["Alcohol"].apply(lambda row: calculate_alcohol_density(row))

    df["Nicotine"] = df["properties~Nicotine~multi_select"].apply(lambda row: get_names(row))
    df.drop("properties~Nicotine~multi_select", axis=1, inplace=True)
    df["Nicotine-Intake"] = df["Nicotine"].apply(lambda row: calculate_nicotine_density(row))

    df.replace("", np.nan, inplace=True)
    df.reset_index(inplace=True)
    return df


@cache.memoize()
def get_complete_data():
    logger.info("Loading data from Notion")
    df = get_database(DATABASE_ID)
    logger.info("Cleaning data")
    df = initial_clean(df)
    logger.info("Data loaded")
    return df
