from google_play_scraper import app, Sort, reviews_all
from apple_store_scraper import AppStore
import pandas as pd
import numpy as np
import json, os, uuid
import gspread
from oauth2client.service_account import ServiceAccountCredentials

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]
creds = ServiceAccountCredentials.from_json_keyfile_name("gs_credentials.json", SCOPES)
client = gspread.authorize(creds)
sheet = client.open("Scraper reviews store")


def main():
    # Google Play
    google_app_name = ["superchinese"]
    google_appIds = ["com.superchinese"]
    google_langs = ["vi"]
    google_countries = ["vn"]
    # Apple Store
    apple_app_name = ["superchinese"]
    apple_appIds = ["1462500984"]
    apple_countries = ["vn"]
    length = len(google_app_name)
    # Scrape
    for i in range(length):
        google_play_scraper(
            google_appIds[i], google_app_name[i], google_langs[i], google_countries[i]
        )

    for i in range(length):
        apple_store_scraper(apple_appIds[i], apple_app_name[i], apple_countries[i])


def google_play_scraper(app_id, app_name, lang, country):
    g_reviews = reviews_all(
        app_id=app_id,
        lang=lang,
        country=country,
        sort=Sort.NEWEST,
        sleep_milliseconds=1000,
    )
    g_df = pd.DataFrame(g_reviews)
    g_df.drop(
        columns=[
            "userImage",
            "reviewCreatedVersion",
            "repliedAt",
            "replyContent",
            "at",
        ],
        inplace=True,
    )
    g_df.rename(
        columns={
            "reviewId": "id",
            "userName": "user_name",
            "content": "review",
            "thumbsUpCount": "thumbs_up_count",
            "appVersion": "app_version",
        },
        inplace=True,
    )

    key = f"GOOGLEPLAY_{app_name}_{lang}_{country}"
    try:
        worksheet = sheet.worksheet(key)
        worksheet.clear()
    except gspread.exceptions.WorksheetNotFound:
        worksheet = sheet.add_worksheet(title=key, rows=100, cols=20)
    worksheet.update([g_df.columns.tolist()] + g_df.values.tolist())

    # Apply formatting: bold title and blue background
    cell_format = {
        "textFormat": {
            "bold": True,
            "foregroundColor": {"red": 0.0, "green": 0.0, "blue": 0.0, "alpha": 1.0},
        },
        "backgroundColor": {"red": 0.0, "green": 1.0, "blue": 0.0, "alpha": 1.0},
        "horizontalAlignment": "CENTER",
    }
    worksheet.format("A1:F1", cell_format)


def apple_store_scraper(app_id, app_name, country):
    app_store = AppStore(country=country, app_name=app_name, app_id=app_id)
    app_store.review()
    a_df = pd.DataFrame(app_store.reviews)
    if "developerResponse" in a_df.columns:
        a_df = a_df[a_df["developerResponse"].isnull()]
    a_df.drop(columns=["isEdited", "date"], inplace=True)
    a_df.rename(
        columns={
            "rating": "score",
            "userName": "user_name",
        },
        inplace=True,
    )
    a_df.dropna(inplace=True)
    a_df.insert(0, "id", uuid.uuid4().hex)
    # Move columns
    a_df.insert(1, "user_name", a_df.pop("user_name"))
    key = f"APPLESTORE_{app_name}_{country}"
    try:
        worksheet = sheet.worksheet(key)
        worksheet.clear()
    except gspread.exceptions.WorksheetNotFound:
        worksheet = sheet.add_worksheet(title=key, rows=100, cols=20)
    worksheet.update([a_df.columns.tolist()] + a_df.values.tolist())

    # Apply formatting: bold title and blue background
    cell_format = {
        "textFormat": {
            "bold": True,
            "foregroundColor": {"red": 1.0, "green": 1.0, "blue": 1.0, "alpha": 1.0},
        },
        "backgroundColor": {"red": 0.0, "green": 0.0, "blue": 1.0, "alpha": 1.0},
        "horizontalAlignment": "CENTER",
    }
    worksheet.format("A1:E1", cell_format)


if __name__ == "__main__":
    main()
