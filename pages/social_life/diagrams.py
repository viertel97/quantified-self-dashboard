import os
from datetime import datetime

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from plotly_calplot import calplot

from pages.social_life.data import get_occurence_calendar_data, get_occurence_data


def generate_scatter_diagram(df, scatter_range):
    data = []
    names = [x for x in df.complete_name.unique() if x is not None]
    for unique_name in np.sort(names):
        temp_df = df[df.complete_name == unique_name]
        if len(temp_df) > scatter_range[0] and len(temp_df) < scatter_range[1]:
            scatter = go.Scatter(
                x=temp_df["happened_at"],
                y=temp_df["complete_name"],
                customdata=temp_df[["summary"]],
                hovertemplate='<a href="google.de">%{y}</a><extra><b>%{customdata[0]}</b></extra>',
                name=unique_name,
                hoverinfo="x+y",
                mode="markers",
            )
            data.append(scatter)

    layout = go.Layout(title="Social Life")

    fig = make_subplots()

    for d in data:
        fig.add_trace(d, secondary_y=False, row=1, col=1)

    fig.update_layout(layout)
    fig.update_layout(hovermode="x unified", hoverdistance=1, yaxis_showticklabels=False)

    fig.update_yaxes(title_text="People")
    fig.update_xaxes(title_text="Dates", type="date")
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
    fig.add_vline(
        x=datetime.today().replace(hour=0, minute=0, second=0), line_width=1, line_dash="dash", line_color="green"
    )
    fig.update_xaxes(showspikes=True, spikecolor="green", spikesnap="cursor", spikemode="across")

    return fig


def generate_pie_diagram(df, pie_range):
    counts = df.complete_name.value_counts()
    counts = pd.DataFrame(counts.index, counts.values)
    counts.reset_index(inplace=True)
    counts = counts.rename(columns={"index": "Count", 0: "Name"})
    counts = counts[(counts["Count"] >= pie_range[0]) & (counts["Count"] <= pie_range[1])]
    counts = counts.sort_values(by="Count", ascending=False)
    fig = px.pie(counts, names="Name", values="Count", title="Social Life")
    fig.update_traces(textposition="inside", textinfo="percent+label")
    fig.update_layout(margin=dict(t=0, b=0, l=0, r=0))
    # fig.update_traces(
    #     hoverinfo="label+percent",
    #     textinfo="value",
    #     textfont_size=20,
    # )
    # fig.update_layout(uniformtext_minsize=5, uniformtext_mode="hide")
    return fig


def generate_occurence_calendar(df):
    data = get_occurence_calendar_data(df)

    fig = calplot(data, x="Date", y="Count", years_title=True)
    # fig.update_traces(
    #     customdata=data["combined_activity"],  # we have to first stack the columns along the last axis
    #     hovertemplate="Date: %{x|%d, %m}<br>Count: %{y:.0f}<br>Events:<br>%{customdata[0]}" + "<extra></extra>",
    # ),
    return fig


def generate_occurence(df, occurence_range):
    data = get_occurence_data(df, occurence_range)

    fig = px.scatter(
        data,
        x="Date",
        y="Count",
        title="Social Life",
        trendline="ols",
        trendline_color_override="black",
    )
    if occurence_range == "Week":
        fig.update_layout(xaxis_tickformat="KW%U<br>%Y")
        fig.update_traces(
            customdata=data[["Start-Date", "End-Date"]],
            mode="lines",
            hovertemplate="<b>KW%{x|%U, %Y} (%{customdata[0]|%d.%m} - %{customdata[1]|%d.%m})</b><br>"
            + "Count: %{y}<br>"
            + "<extra></extra>",
        )
    else:
        fig.update_traces(
            mode="lines",
            hovertemplate="<b>%{x|%B, %Y}</b><br>" + "Count: %{y}<br>" + "<extra></extra>",
        )

    fig.update_yaxes(title_text="Drug")
    fig.update_xaxes(title_text=occurence_range)
    return fig
