import os

from dash import dcc, html
from loguru import logger

from pages.drug_tracker.diagrams import (
    generate_intake_diagram,
    generate_occurence_diagram,
)
from pages.drug_tracker.kpi import get_kpi_values

logger.add(
    os.path.join(os.path.dirname(os.path.abspath(__file__)) + "/logs/" + os.path.basename(__file__) + ".log"),
    format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}",
    backtrace=True,
    diagnose=True,
)


def get_occurence_view(df, relevant_columns, occurence_range=None):
    return_list = []
    return_list.append(
        dcc.Graph(
            figure=generate_occurence_diagram(
                df,
                occurence_range,
                relevant_columns,
            ),
            id="drug-diagram",
        )
    )
    return_list.append(
        html.Div(
            get_kpi_values(df, relevant_columns),
            style={"display": "flex", "flex-wrap": "wrap", "justify-content": "center"},
            id="drug-kpi",
        )
    )
    return return_list


def get_intake_view(df, relevant_columns):
    return_list = []
    return_list.append(
        dcc.Graph(
            figure=generate_intake_diagram(df, relevant_columns),
            id="drug-diagram",
        )
    )
    return_list.append(
        html.Div(
            get_kpi_values(df, relevant_columns),
            style={"display": "flex", "flex-wrap": "wrap", "justify-content": "center"},
            id="drug-kpi",
        )
    )
    return return_list
