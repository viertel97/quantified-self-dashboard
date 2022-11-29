import os

from dash import dcc, html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from loguru import logger

from app import app
from pages.social_life.data import get_complete_data, get_pie_boundries
from pages.social_life.kpi import get_kpi_values
from pages.social_life.view import (
    get_occurence_calendar_view,
    get_occurence_view,
    get_pie_view,
    get_scatter_view,
)

logger.add(
    os.path.join(os.path.dirname(os.path.abspath(__file__)) + "/logs/" + os.path.basename(__file__) + ".log"),
    format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}",
    backtrace=True,
    diagnose=True,
)

DF = get_complete_data()
boundries = get_pie_boundries(DF)


@app.callback(
    Output("social-diagram-container", "children"),
    [
        Input("social-type", "value"),
        Input("social-scatter-range", "value"),
        Input("social-occurence-range", "value"),
        Input("social-pie-range", "value"),
    ],
)
def update_intake(
    diagram_type,
    scatter_range=None,
    occurence_range=None,
    pie_range=None,
):
    if diagram_type == "Pie":
        return get_pie_view(DF, pie_range)
    if diagram_type == "Occurence":
        return get_occurence_view(DF, occurence_range)
    elif diagram_type == "Scatter":
        return get_scatter_view(DF, scatter_range)
    elif diagram_type == "Calendar":
        return get_occurence_calendar_view(DF)


@app.callback(
    Output("social-kpi", "children"),
    [
        Input("update-social-kpi", "value"),
    ],
)
def update_kpi(relayout_data):
    if (
        relayout_data is None
        or "xaxis.range[0]" not in relayout_data.keys()
        or "xaxis.range[1]" not in relayout_data.keys()
    ):
        return html.Div(
            get_kpi_values(DF),
            style={"display": "flex", "flex-wrap": "wrap", "justify-content": "center"},
        )
    else:
        return html.Div(
            get_kpi_values(DF, relayout_data),
            style={"display": "flex", "flex-wrap": "wrap", "justify-content": "center"},
        )


@app.callback(Output("update-social-kpi", "value"), Input("social-diagram", "relayoutData"))
def test(relayoutData):
    if relayoutData is not None:
        return relayoutData
    else:
        raise PreventUpdate


layout = html.Div(
    [
        dcc.Store(id="update-social-kpi"),
        dcc.Tabs(
            [
                dcc.Tab(
                    label="Scatter",
                    value="Scatter",
                    children=[
                        dcc.RangeSlider(
                            boundries[0], boundries[1], value=[boundries[0], boundries[1]], id="social-scatter-range"
                        )
                    ],
                ),
                dcc.Tab(
                    label="Occurence",
                    value="Occurence",
                    children=[
                        dcc.Dropdown(
                            ["Month", "Week"],
                            "Month",
                            id="social-occurence-range",
                        ),
                    ],
                ),
                dcc.Tab(
                    label="Occurence Calendar",
                    value="Calendar",
                    children=[],
                ),
                dcc.Tab(
                    label="Pie",
                    value="Pie",
                    children=[
                        dcc.RangeSlider(
                            boundries[0], boundries[1], value=[boundries[0], boundries[1]], id="social-pie-range"
                        )
                    ],
                ),
            ],
            id="social-type",
            value="Occurence",
        ),
        html.Div(id="social-diagram-container"),
        html.Br(),
        html.Div(
            [
                dcc.Loading(id="loading-1", type="default", children=html.Div(id="loading-output-1")),
            ]
        ),
    ]
)
