import os
from datetime import datetime

import dash_bootstrap_components as dbc
from dash import html
from dateutil import parser
from loguru import logger

from pages.social_life.data import get_occurence_data

logger.add(
    os.path.join(os.path.dirname(os.path.abspath(__file__)) + "/logs/" + os.path.basename(__file__) + ".log"),
    format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}",
    backtrace=True,
    diagnose=True,
)


def get_kpi_values(df, relayout_data=None):
    return_array = []
    if relayout_data is not None:
        start = parser.parse(relayout_data["xaxis.range[0]"])
        end = parser.parse(relayout_data["xaxis.range[1]"])
        df = df[(df["happened_at"] >= start) & (df["happened_at"] <= end)]
    counts = get_occurence_data(df, "Month")
    per_month = counts["Count"].sum() / counts["Count"].count()
    per_week = per_month / 4
    return_array.append(
        dbc.Card(
            [
                dbc.CardHeader("Social Interactions"),
                dbc.CardBody(
                    [
                        html.P(
                            "{per_week} per Week | {per_month} per Month".format(
                                per_week=str(round(per_week, 1)), per_month=str(round(per_month, 1))
                            ),
                            className="card-text",
                        )
                    ]
                ),
            ],
            style={"width": "18rem"},
        )
    )
    return return_array
