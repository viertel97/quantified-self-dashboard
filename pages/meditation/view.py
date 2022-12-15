import os

from dash import dcc, html
from loguru import logger

from pages.meditation.diagrams import (
    get_meditation_occurrence_diagram,
    get_meditation_calendar_diagram,
)
from pages.meditation.kpi import get_kpi_values

logger.add(
    os.path.join(os.path.dirname(os.path.abspath(__file__)) + "/logs/" + os.path.basename(__file__) + ".log"),
    format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}",
    backtrace=True,
    diagnose=True,
)


def get_occurrence_view(df):
    return_list = []
    return_list.append(
        dcc.Graph(
            figure=get_meditation_occurrence_diagram(
                df,
            ),
            id="meditation-diagram",
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

def get_calendar_view(df):
    return_list = []
    return_list.append(
        dcc.Graph(
            figure=get_meditation_calendar_diagram(
                df,
            ),
            id="meditation-diagram",
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