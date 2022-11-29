import os

from dash import dcc, html
from loguru import logger

from pages.social_life.diagrams import (
    generate_occurence,
    generate_occurence_calendar,
    generate_pie_diagram,
    generate_scatter_diagram,
)
from pages.social_life.kpi import get_kpi_values

logger.add(
    os.path.join(os.path.dirname(os.path.abspath(__file__)) + "/logs/" + os.path.basename(__file__) + ".log"),
    format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}",
    backtrace=True,
    diagnose=True,
)


def get_pie_view(df, pie_range=None):
    return_list = []
    return_list.append(
        dcc.Graph(
            figure=generate_pie_diagram(df, pie_range),
            id="social-diagram",
        )
    )
    return return_list


def get_scatter_view(df, scatter_range=None):
    return_list = []
    return_list.append(
        dcc.Graph(
            figure=generate_scatter_diagram(df, scatter_range),
            id="social-diagram",
        )
    )
    return_list.append(
        html.Div(
            get_kpi_values(df),
            style={"display": "flex", "flex-wrap": "wrap", "justify-content": "center"},
            id="social-kpi",
        )
    )
    return return_list


def get_occurence_calendar_view(df):
    return_list = []
    return_list.append(
        dcc.Graph(
            figure=generate_occurence_calendar(
                df,
            ),
            id="social-diagram",
        )
    )
    return return_list


def get_occurence_view(df, occurence_range=None):
    return_list = []
    return_list.append(
        dcc.Graph(
            figure=generate_occurence(
                df,
                occurence_range,
            ),
            id="social-diagram",
        )
    )
    return_list.append(
        html.Div(
            get_kpi_values(df),
            style={"display": "flex", "flex-wrap": "wrap", "justify-content": "center"},
            id="social-kpi",
        )
    )
    return return_list
