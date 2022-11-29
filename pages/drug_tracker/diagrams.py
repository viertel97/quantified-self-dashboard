import calendar
import os
from datetime import datetime

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from loguru import logger
from plotly.subplots import make_subplots

logger.add(
    os.path.join(os.path.dirname(os.path.abspath(__file__)) + "/logs/" + os.path.basename(__file__) + ".log"),
    format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}",
    backtrace=True,
    diagnose=True,
)


def generate_intake_diagram(df, relevant_columns):
    data = get_intake_data(df, relevant_columns)

    layout = go.Layout(barmode="stack", title="Drug-Tracker")

    fig = make_subplots(specs=[[{"secondary_y": False}]])
    for d in data:
        fig.add_trace(d, secondary_y=False, row=1, col=1)

    fig.update_layout(layout)
    fig.update_layout(hovermode="x unified", hoverdistance=14, yaxis_showticklabels=False)

    fig.update_yaxes(title_text="Drug")
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
    return fig


def generate_occurence_diagram(df, occurance_range, relevant_columns):
    data = get_occurence_data(df, occurance_range, relevant_columns)

    fig = px.scatter(
        data,
        x="Date",
        y=relevant_columns,
        title="Drug-Tracker",
        trendline="ols",
        trendline_color_override="black",
    )
    fig.update_traces(mode="lines")

    fig.update_yaxes(title_text="Drug")
    fig.update_xaxes(title_text=occurance_range)
    return fig


def get_occurence_data(df, occurance_range, relevant_columns):
    temp = pd.DataFrame()
    if occurance_range == "Month":
        temp["Date"] = df["Alcohol"].groupby([df.Date.dt.month]).agg("count").index
        temp["Date"] = temp["Date"].apply(lambda x: datetime.strptime(str(x) + "-" + str(datetime.now().year), "%m-%Y"))
        for col in relevant_columns:
            temp[col] = df[col].groupby([df.Date.dt.month]).agg("count").values
    else:
        temp["Date"] = df["Alcohol"].groupby([df.Date.dt.strftime("%W")]).agg("count").index
        for col in relevant_columns:
            temp[col] = df[col].groupby([df.Date.dt.strftime("%W")]).agg("count").values
    return temp


def get_intake_data(df, relevant_columns):
    data = [
        go.Bar(
            x=df["Date"],  # assign x as the dataframe column 'x'
            y=df["Alcohol-Intake"] * 0.01,
            customdata=df[["Alcohol-Intake"]],
            name="Alcohol",
            hovertemplate="Gramm: %{customdata[0]:.1f}",
        ),
        go.Bar(
            x=df["Date"],  # assign x as the dataframe column 'x'
            y=df["Nicotine-Intake"],
            name="Nicotine",
            hovertemplate="Shisha-Köpfe: %{y}",
        ),
    ]
    return data
