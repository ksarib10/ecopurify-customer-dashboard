from datetime import datetime, date

"""
Utility helpers for:
1) Date calculations
2) Service-based health degradation
"""


def days_since(date_str):
    """
    Returns number of days passed since the given date string.
    If date is missing or invalid, returns 0.

    Supported formats:
    - YYYY-MM-DD
    - YYYY/MM/DD
    - DD-MM-YYYY
    - DD/MM/YYYY
    - YYYY-MM-DD HH:MM:SS
    """

    if not date_str:
        return 0

    date_str = str(date_str).strip()

    allowed_formats = [
        "%Y-%m-%d",
        "%Y/%m/%d",
        "%d-%m-%Y",
        "%d/%m/%Y",
        "%Y-%m-%d %H:%M:%S",
    ]

    for fmt in allowed_formats:
        try:
            last_service_date = datetime.strptime(date_str, fmt).date()
            return (date.today() - last_service_date).days
        except ValueError:
            continue

    # If all formats fail
    print("❌ DATE PARSE FAILED:", date_str)
    return 0


def health_from_days(days):
    """
    Derives health status purely from days since last service.

    Rules:
    - < 35 days   → Excellent
    - ≥ 35 days   → Good
    - ≥ 45 days   → Average
    - ≥ 60 days   → Needs Attention
    """

    if days >= 60:
        return "Needs Attention"
    if days >= 45:
        return "Average"
    if days >= 35:
        return "Good"

    return "Excellent"
