import os
from quarter_lib.akeyless import get_secrets

NOTION_API_KEY = get_secrets(["notion/token"])
BASE_URL = "https://api.notion.com/v1/"
HEADERS = {
    "Authorization": "Bearer " + NOTION_API_KEY,
    "Content-Type": "application/json",
    "Notion-Version": "2021-08-16",
}
DATABASE_ID = "2df7057b7dc64fc6a48884db6e9bd28d"

ALCOHOL_DICT = {
    "Bier": 13.2,
    "Biermixgetränk": 6.6,
    "Wein": 24,
    "Schaumwein": 17.6,
    "Shot": 6.08,
    "Longdrink": 12.16,
    "Cocktail": 18.24,
}
NICOTINE_DICT = {
    "Shisha-Kopf": 1,
}
