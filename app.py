import dash
import dash_bootstrap_components as dbc
from flask_caching import Cache

# meta_tags are required for the app layout to be mobile responsive
app = dash.Dash(
    __name__,
    suppress_callback_exceptions=True,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1.0"}],
)
cache = Cache(
    app.server, config={"CACHE_TYPE": "filesystem", "CACHE_DIR": "cache-directory", "CACHE_DEFAULT_TIMEOUT": 300}
)
server = app.server
