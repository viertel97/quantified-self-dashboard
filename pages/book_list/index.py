from dash import html

from app import app
from pages.book_list.constants import EMBED_URL

layout = (
    html.Iframe(
        src=EMBED_URL,
        style={"border": 0, "padding": 0, "margin": 0, "width": "100%", "height": "100vh", "overflow": "hidden"},
    ),
)
