from datetime import datetime, timedelta


def get_start_date(days_ago) -> datetime:
    """
    Get the date from X days ago.

    :param days_ago: number of days ago
    :return: date from X number days ago
    """
    return datetime.today() - timedelta(days=days_ago)


def format_date(date: datetime) -> str:
    """
    Format date to dd/mm/yyyy.

    :param date: date to format
    :return: formatted date as str
    """
    return f"{date.day}/{date.month}/{date.year}"
