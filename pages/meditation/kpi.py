import os

import dash_bootstrap_components as dbc
from dash import html
from dateutil import parser
from loguru import logger

from pages.meditation.data import get_occurrence_diagram_data

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
        df = df[(df["start"] >= start) & (df["start"] <= end)]
    counts = get_occurrence_diagram_data(df)
    per_day = counts["Count"].sum() / counts["Count"].count()
    per_week = per_day * 7
    per_month = per_week * 4
    return_array.append(
        dbc.Card(
            [
                dbc.CardHeader("Meditation Occurrences"),
                dbc.CardBody(
                    [
                        html.P(
                            "{per_day} per Day | {per_week} per Week | {per_month} per Month | {total} in Total".format(
                                per_day=str(round(per_day, 1)), per_week=str(round(per_week, 1)),
                                per_month=str(round(per_month, 1)), total=str(counts["Count"].sum())
                            ),
                            className="card-text",
                        )

                    ]
                ),
            ],
            style={"width": "18rem"},
        )
    )

    sum = counts["Sum"].sum()
    per_day = sum / counts["Count"].count()
    per_week = per_day * 7
    per_month = per_week * 4
    return_array.append(
        dbc.Card(
            [
                dbc.CardHeader("Meditation Time"),
                dbc.CardBody(
                    [
                        html.P(
                            "{per_day} per Day ".format(
                                per_day=td_format(per_day)
                            ),
                            className="card-text",
                        ),
                        html.P(
                            "{per_week} per Week".format(
                                per_week=td_format(per_week),
                            ),
                            className="card-text",
                        ),
                        html.P(
                            "{per_month} per Month".format(
                                per_month=td_format(per_month),
                            ),
                            className="card-text",
                        ),
                        html.P(
                            "{total} in Total".format(
                                total=td_format(counts["Sum"].sum())
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


def td_format(seconds):
    periods = [
        ('year', 60 * 60 * 24 * 365),
        ('month', 60 * 60 * 24 * 30),
        ('day', 60 * 60 * 24),
        ('hour', 60 * 60),
        ('minute', 60),
        ('second', 1)
    ]

    strings = []
    for period_name, period_seconds in periods:
        if seconds > period_seconds:
            period_value, seconds = divmod(seconds, period_seconds)
            has_s = 's' if period_value > 1 else ''
            strings.append("%s %s%s" % (period_value, period_name, has_s))

    return ", ".join(strings)
