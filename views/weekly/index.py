import dash_core_components as dcc
import dash_html_components as html

from app import app
from pages.drug_tracker.data import get_complete_data
from pages.drug_tracker.diagrams import intake_diagram

view = html.Div([])
