import os
from datetime import datetime

import dash_bootstrap_components as dbc
from dash import html
from dateutil import parser
from loguru import logger

logger.add(
    os.path.join(os.path.dirname(os.path.abspath(__file__)) + "/logs/" + os.path.basename(__file__) + ".log"),
    format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}",
    backtrace=True,
    diagnose=True,
)


def get_kpi_values(df, relevant_columns, relayout_data=None):
    return_array = []
    if relayout_data is not None:
        start = parser.parse(relayout_data["xaxis.range[0]"])
        end = parser.parse(relayout_data["xaxis.range[1]"])
        df = df[(df["Date"] >= start) & (df["Date"] <= end)]
    counts = df.count()
    for col in relevant_columns:
        per_month = counts[col] / 12
        per_week = per_month / 4
        return_array.append(
            dbc.Card(
                [
                    dbc.CardHeader(col),
                    dbc.CardBody(
                        [
                            html.H5(str(counts[col]) + " Intakes", className="card-title"),
                            html.P(
                                "{per_week} per Week | {per_month} per Month".format(
                                    per_week=str(round(per_week, 1)), per_month=str(round(per_month, 1))
                                ),
                                className="card-text",
                            )
                            if relayout_data is None
                            else html.Div(),
                        ]
                    ),
                ],
                style={"width": "18rem"},
            )
        )
    return return_array
