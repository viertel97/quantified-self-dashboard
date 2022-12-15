import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.dependencies import Input, Output

from app import app, server
from pages.book_list import index as book_list
from pages.drug_tracker import index as drug_tracker
from pages.meditation import index as meditation

# Connect to your app pages
from pages.home import index as home
from pages.social_life import index as social_life
from tools.helper import get_debug, get_ip

app.layout = html.Div(
    [
        dcc.Location(id="url", refresh=False),
        dbc.NavbarSimple(
            children=[
                dbc.NavItem(dbc.NavLink("Drug Tracker", href="/drug-tracker")),
                dbc.NavItem(dbc.NavLink("Social Life", href="/social-life")),
                dbc.NavItem(dbc.NavLink("Book-List", href="/book-list")),
                dbc.NavItem(dbc.NavLink("Meditation", href="/meditation")),
            ],
            brand="Home",
            brand_href="/",
            color="primary",
            dark=True,
        ),
        html.Div(id="page-content", children=[]),
    ]
)


@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def display_page(pathname):
    if pathname == "/drug-tracker":
        return drug_tracker.layout
    if pathname == "/social-life":
        return social_life.layout
    if pathname == "/book-list":
        return book_list.layout
    if pathname == "/meditation":
        return meditation.layout
    else:
        return home.layout


if __name__ == "__main__":
    app.run_server(get_ip(), port=8060, debug=get_debug())
