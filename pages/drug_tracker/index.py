import os
from datetime import datetime

from dash import dcc, html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from loguru import logger

from app import app
from pages.drug_tracker.data import get_complete_data
from pages.drug_tracker.kpi import get_kpi_values
from pages.drug_tracker.view import get_intake_view, get_occurence_view

logger.add(
    os.path.join(os.path.dirname(os.path.abspath(__file__)) + "/logs/" + os.path.basename(__file__) + ".log"),
    format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}",
    backtrace=True,
    diagnose=True,
)

DF = get_complete_data()


def get_columns():
    return ["Alcohol", "Nicotine"]


@app.callback(
    Output("drug-diagram-container", "children"),
    [
        Input("drug-type", "value"),
        Input("occurence-range", "value"),
    ],
)
def update_intake(diagram_type, occurence_range=None):
    relevant_columns = get_columns()
    if diagram_type == "Occurence":
        return get_occurence_view(DF, relevant_columns, occurence_range)
    elif diagram_type == "Intake":
        return get_intake_view(DF, relevant_columns)


@app.callback(
    Output("drug-kpi", "children"),
    [
        Input("update-kpi", "value"),
    ],
)
def update_kpi(relayout_data):
    relevant_columns = get_columns()
    if (
        relayout_data is None
        or "xaxis.range[0]" not in relayout_data.keys()
        or "xaxis.range[1]" not in relayout_data.keys()
    ):
        return html.Div(
            get_kpi_values(DF, relevant_columns),
            style={"display": "flex", "flex-wrap": "wrap", "justify-content": "center"},
        )
    else:
        return html.Div(
            get_kpi_values(DF, relevant_columns, relayout_data),
            style={"display": "flex", "flex-wrap": "wrap", "justify-content": "center"},
        )


@app.callback(Output("update-drug-kpi", "value"), Input("drug-diagram", "relayoutData"))
def test(relayoutData):
    if relayoutData is not None:
        return relayoutData
    else:
        raise PreventUpdate


layout = html.Div(
    [
        dcc.Store(id="update-drug-kpi"),
        dcc.Tabs(
            [
                dcc.Tab(
                    label="Occurence",
                    value="Occurence",
                    children=[
                        dcc.Dropdown(
                            ["Month", "Week"],
                            "Month",
                            id="occurence-range",
                        ),
                    ],
                ),
                dcc.Tab(
                    label="Intake",
                    value="Intake",
                    children=[],
                ),
            ],
            id="drug-type",
            value="Occurence",
        ),
        html.Div(id="drug-diagram-container"),
        html.Br(),
        html.Div(
            [
                dcc.Loading(id="loading-1", type="default", children=html.Div(id="loading-output-1")),
            ]
        ),
    ]
)
