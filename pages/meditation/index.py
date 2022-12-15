from dash import dcc, html
from dash.dependencies import Input, Output

from app import app
from pages.meditation.data import get_complete_data
from pages.meditation.kpi import get_kpi_values
from pages.meditation.view import get_occurrence_view, get_calendar_view

DF = get_complete_data()


@app.callback(
    Output("meditation-diagram-container", "children"),
    [
        Input("meditation-type", "value"),
    ],
)
def update_intake(diagram_type):
    if diagram_type == "Occurrence":
        return get_occurrence_view(DF)
    elif diagram_type == "Calendar":
        return get_calendar_view(DF)


@app.callback(
    Output("meditation-kpi", "children"),
    [
        Input("meditation-social-kpi", "value"),
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


layout = html.Div(
    [
        dcc.Store(id="update-meditation-kpi"),
        dcc.Tabs(
            [
                dcc.Tab(
                    label="Occurrence",
                    value="Occurrence",
                    children=[],
                ),
                dcc.Tab(
                    label="Calendar",
                    value="Calendar",
                    children=[],
                ),
            ],
            id="meditation-type",
            value="Occurrence",
        ),
        html.Br(),
        html.Div(id="meditation-diagram-container"),
        html.Div(
            [
                dcc.Loading(id="loading-1", type="default", children=html.Div(id="loading-output-1")),
            ]
        ),
    ]
)
