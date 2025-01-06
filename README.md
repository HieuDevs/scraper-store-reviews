# Scraper Store Reviews

This project is designed to scrape app reviews from Google Play and Apple Store, and store the data in Google Sheets. The project utilizes `gspread` for Google Sheets integration and `oauth2client` for authentication.

## Project Structure

- `main.py`: The main script that handles the scraping and data storage.
- `.gitignore`: Specifies files and directories to be ignored by git.
- `README.md`: Project documentation.
- `pyproject.toml`: Project metadata and dependencies.

## Dependencies

- `google_play_scraper`
- `apple_store_scraper`
- `pandas`
- `numpy`
- `gspread`
- `oauth2client`

## Setup

1. Clone the repository:

    ```sh
    git clone <repository_url>
    cd scraper-store-reviews
    ```

2. Create a virtual environment and activate it:

    ```sh
    python -m venv .venv
    source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`
    ```

3. Install the dependencies:

    ```sh
    pip install -r requirements.txt
    ```

4. Set up Google Sheets API credentials:
    - Create a project in the [Google Developers Console](https://console.developers.google.com/).
    - Enable the Google Sheets API and Google Drive API.
    - Create a service account and download the JSON key file.
    - Rename the JSON key file to `gs_credentials.json` and place it in the project root directory.

## Usage

Run the main script to start scraping reviews and storing them in Google Sheets:
