import os
from datetime import datetime

import pandas as pd
from loguru import logger
from quarter_lib_old.database import (
    close_server_connection,
    create_monica_server_connection,
)


logger.add(
    os.path.join(os.path.dirname(os.path.abspath(__file__)) + "/logs/" + os.path.basename(__file__) + ".log"),
    format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}",
    backtrace=True,
    diagnose=True,
)
from app import cache


# @cache.memoize()
def get_activities_db():
    connection = create_monica_server_connection()
    df = pd.read_sql_query(
        """  SELECT act.id, act.summary, act.happened_at, CONCAT(c.first_name," ",c.last_name) as complete_name 
                                FROM activities act
                                INNER JOIN activity_contact ac ON act.id=ac.activity_id
                                INNER JOIN contacts c ON ac.contact_id = c.id
                                ORDER BY act.happened_at
                                """,
        connection,
    )
    close_server_connection(connection)
    return df


@cache.memoize()
def get_complete_data():
    logger.info("load social life data")
    df = get_activities_db()
    df = df[df.complete_name.notna()]
    df.drop(columns=["id"], inplace=True)
    df["happened_at"] = pd.to_datetime(df["happened_at"])
    logger.info("found " + str(len(df)) + " activities")
    return df


@cache.memoize()
def get_pie_boundries(df):
    counts = df.complete_name.value_counts()
    return counts.min(), counts.max()


@cache.memoize()
def get_occurence_data(df, occurance_range):
    if occurance_range == "Month":
        grouped = df.groupby([df.happened_at.dt.year, df.happened_at.dt.month]).agg([lambda x: list(x), "count"])
    else:
        grouped = df.groupby([df.happened_at.dt.year, df.happened_at.dt.strftime("%W")]).agg(
            [lambda x: list(x), "count"]
        )
    grouped_df = pd.DataFrame(grouped)
    grouped_df.index = grouped_df.index.to_flat_index()
    grouped_df.columns = grouped_df.columns.to_flat_index()
    grouped_df.reset_index(drop=False, inplace=True)
    if occurance_range == "Month":
        grouped_df["Date"] = grouped_df["index"].apply(lambda x: datetime(x[0], x[1], 1))
    else:
        grouped_df["Date"] = grouped_df["index"].apply(
            lambda x: datetime.strptime(str(x[0]) + "-" + str(x[1] + "-4"), "%G-%V-%u")
        )
        grouped_df["Start-Date"] = grouped_df["Date"].apply(lambda x: x - pd.Timedelta(days=3))
        grouped_df["End-Date"] = grouped_df["Date"].apply(lambda x: x + pd.Timedelta(days=3))
    grouped_df.rename(
        columns={
            ("summary", "<lambda_0>"): "Activity",
            ("complete_name", "<lambda_0>"): "Participants",
        },
        inplace=True,
    )
    grouped_df["Count"] = grouped_df.apply(lambda x: len(set(x["Activity"])), axis=1)

    grouped_df.drop(
        columns=[
            "index",
            ("happened_at", "count"),
            ("happened_at", "<lambda_0>"),
            ("complete_name", "count"),
            ("summary", "count"),
        ],
        inplace=True,
    )
    grouped_df["combined_activity"] = grouped_df.apply(
        lambda x: combine_columns(x["Activity"], x["Participants"]), axis=1
    )
    grouped_df.drop(columns=["Activity", "Participants"], inplace=True)
    #    temp["Date"] = df["happened_at"].groupby([df.happened_at.dt.month]).agg("count").index
    #    temp["Date"] = temp["Date"].apply(lambda x: datetime.strptime(str(x) + "-" + str(datetime.now().year), "%m-%Y"))
    #    # for col in relevant_columns:
    #    #    temp[col] = df[col].groupby([df.Date.dt.month]).agg("count").values
    # else:
    #    # for col in relevant_columns:
    #    #    temp[col] = df[col].groupby([df.Date.dt.strftime("%W")]).agg("count").values

    return grouped_df


def combine_columns(activity_list, participants_list):
    end_list = []
    for activity, participants in zip(activity_list, participants_list):
        end_list.append(f"{activity} ({participants})\n")
    return end_list


@cache.memoize()
def get_occurence_calendar_data(df):
    grouped = df.groupby([df.happened_at.dt.year, df.happened_at.dt.month, df.happened_at.dt.day]).agg(
        [lambda x: list(x), "count"]
    )
    grouped_df = pd.DataFrame(grouped)
    grouped_df.index = grouped_df.index.to_flat_index()
    grouped_df.columns = grouped_df.columns.to_flat_index()
    grouped_df.reset_index(drop=False, inplace=True)
    grouped_df["Date"] = grouped_df["index"].apply(lambda x: datetime(x[0], x[1], x[2]))
    grouped_df.rename(
        columns={
            ("summary", "<lambda_0>"): "Activity",
            ("complete_name", "<lambda_0>"): "Participants",
        },
        inplace=True,
    )
    grouped_df["Count"] = grouped_df.apply(lambda x: len(set(x["Activity"])), axis=1)

    grouped_df.drop(
        columns=[
            "index",
            ("happened_at", "count"),
            ("happened_at", "<lambda_0>"),
            ("complete_name", "count"),
            ("summary", "count"),
        ],
        inplace=True,
    )
    grouped_df["combined_activity"] = grouped_df.apply(
        lambda x: combine_columns(x["Activity"], x["Participants"]), axis=1
    )
    grouped_df.drop(columns=["Activity", "Participants"], inplace=True)
    return grouped_df
