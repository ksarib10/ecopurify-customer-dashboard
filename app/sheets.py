"""
Google Sheets data access layer.

All direct interactions with Google Sheets
should live in this file.
"""

import gspread
from google.oauth2.service_account import Credentials
from config import SCOPES, CREDS_FILE, SPREADSHEET_ID, SHEET_NAME


# -------------------------
# Sheet Connection
# -------------------------

def get_sheet():
    """
    Authorizes and returns the worksheet instance.
    """
    creds = Credentials.from_service_account_file(
        CREDS_FILE,
        scopes=SCOPES
    )
    client = gspread.authorize(creds)
    return client.open_by_key(SPREADSHEET_ID).worksheet(SHEET_NAME)


# -------------------------
# Read Operations
# -------------------------

def get_all_rows():
    """
    Returns all records from the sheet as list of dicts.
    """
    sheet = get_sheet()
    return sheet.get_all_records()


def find_plants_by_customer(customer_id):
    """
    Returns all plant rows for a given customer_id.
    """
    records = get_all_rows()
    return [row for row in records if row.get("customer_id") == customer_id]


def find_plant_by_id(plant_id):
    """
    Returns a single plant row by plant_id.
    """
    records = get_all_rows()
    for row in records:
        if row.get("plant_id") == plant_id:
            return row
    return None


# -------------------------
# Write Operations
# -------------------------

def update_health_by_row(row_index, updates):
    """
    Updates health-related columns for a specific sheet row.

    Args:
        row_index (int): Actual row number in sheet (1-based)
        updates (dict): { column_name: new_value }
    """
    sheet = get_sheet()
    headers = sheet.row_values(1)

    for col_name, value in updates.items():
        if col_name not in headers:
            continue
        col_index = headers.index(col_name) + 1
        sheet.update_cell(row_index, col_index, value)
