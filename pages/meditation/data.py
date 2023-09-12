import os
from datetime import datetime

import numpy as np
import pandas as pd
from loguru import logger
from quarter_lib_old.database import (
    close_server_connection,
    create_server_connection,
)

logger.add(
    os.path.join(os.path.dirname(os.path.abspath(__file__)) + "/logs/" + os.path.basename(__file__) + ".log"),
    format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}",
    backtrace=True,
    diagnose=True,
)
from app import cache


@cache.memoize()

def get_complete_data():
    logger.info("load meditation data")
    df = get_meditation_data()
    logger.info("load meditation data done")
    return df

@cache.memoize()

def get_meditation_data():
    connection = create_server_connection()
    df = pd.read_sql_query(
        """  SELECT * FROM meditation""",
        connection,
    )
    close_server_connection(connection)
    return df

@cache.memoize()

def get_meditation_calendar_data(df):
    grouped = df.groupby([df.start.dt.year, df.start.dt.month, df.start.dt.day]).agg(
        Count=('diff_s', np.count_nonzero),
        Sum=('diff_s', np.sum),
        Mean=('diff_s', np.mean))
    grouped_df = pd.DataFrame(grouped)
    grouped_df.index = grouped_df.index.to_flat_index()
    grouped_df.columns = grouped_df.columns.to_flat_index()
    grouped_df.reset_index(drop=False, inplace=True)
    grouped_df["Date"] = grouped_df["index"].apply(lambda x: datetime(x[0], x[1], x[2]))
    return grouped_df

@cache.memoize()

def get_occurrence_diagram_data(df):
    df['diff'] = df['end'] - df['start']
    df['start_date'] = df['start'].dt.date
    df['diff_s'] = df['diff'].dt.total_seconds()
    df['start_time'] = df['start'].dt.time
    df['end_time'] = df['end'].dt.time

    temp = df.groupby([df['start'].dt.date]).agg(
        Count=('diff_s', np.count_nonzero),
        Sum=('diff_s', np.sum),
        Mean=('diff_s', np.mean))

    return temp

def get_occurence_kpi_data(df):
    return df