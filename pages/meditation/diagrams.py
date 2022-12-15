import plotly.graph_objects as go
from plotly.subplots import make_subplots
from plotly_calplot import calplot

from pages.meditation.data import get_meditation_calendar_data, get_occurrence_diagram_data


def get_meditation_occurrence_diagram(df):
    temp = get_occurrence_diagram_data(df)

    data = [(
        go.Scatter(
            x=temp.index,
            y=temp["Count"],
            mode="lines+markers",
            name="Count",
            hovertemplate="<br>".join([
                "Count: %{y}",
            ])
        ), False),
        (go.Scatter(
            x=temp.index,  # assign x as the dataframe column 'x'
            y=temp["Sum"],
            name="Sum",
            mode="lines+markers",
            hovertemplate="<br>".join([
                "Seconds: %{y}",
            ])
        ), True),
    ]

    layout = go.Layout(title="Meditation")

    fig = make_subplots(specs=[[{"secondary_y": True}]])

    for d in data:
        fig.add_trace(d[0], secondary_y=d[1], row=1, col=1)

    fig.update_layout(layout)
    fig.update_layout(hovermode="x unified")
    fig.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    ))
    fig.update_layout(
        yaxis=dict(
            tickmode='linear',
            tick0=0,
            dtick=1
        )
    )
    fig.update_yaxes(title_text="Count", secondary_y=True)
    fig.update_yaxes(title_text="Seconds", secondary_y=False)
    fig.update_xaxes(title_text="Dates")
    fig.update_xaxes(type="date")
    fig.update_xaxes(
        rangeslider_visible=False,
        rangeselector=dict(
            buttons=list(
                [
                    dict(count=7, label="1w", step="day", stepmode="backward"),
                    dict(count=1, label="1m", step="month", stepmode="backward"),
                    dict(count=6, label="6m", step="month", stepmode="backward"),
                    dict(count=1, label="YTD", step="year", stepmode="todate"),
                    dict(count=1, label="1y", step="year", stepmode="backward"),
                    dict(step="all"),
                ]
            )
        ),
        tickformatstops=[
            dict(dtickrange=[None, 604800000], value="%e. %b"),
            dict(dtickrange=[604800000, "M1"], value="%e. %b"),
            dict(dtickrange=["M1", "M12"], value="%b '%y", name="Test"),
            dict(dtickrange=["M12", None], value="%Y"),
        ],
    )

    fig.update_layout(
        yaxis4=dict(showticklabels=False, overlaying="y", anchor="free", position=1, zeroline=True, visible=False)
    )
    return fig


def get_meditation_calendar_diagram(df):
    grouped_df = get_meditation_calendar_data(df)

    fig = calplot(data=grouped_df, x="Date", y="Count", years_title=True)
    return fig
