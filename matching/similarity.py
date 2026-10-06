from difflib import SequenceMatcher
from datetime import datetime


def text_similarity(text1, text2):
    """Return text similarity as a percentage from 0 to 100."""
    if not text1 or not text2:
        return 0.0

    text1 = text1.lower().strip()
    text2 = text2.lower().strip()

    return round(SequenceMatcher(None, text1, text2).ratio() * 100, 2)


def category_similarity(category1, category2):
    """Return category similarity."""
    if not category1 or not category2:
        return 0.0

    return 100.0 if category1.lower().strip() == category2.lower().strip() else 0.0


def location_similarity(location1, location2):
    """Return location similarity."""
    if not location1 or not location2:
        return 0.0

    location1 = location1.lower().strip()
    location2 = location2.lower().strip()

    if location1 == location2:
        return 100.0

    return text_similarity(location1, location2)


def date_similarity(date1, date2):
    """Return date similarity based on difference in days."""
    if not date1 or not date2:
        return 0.0

    try:
        d1 = datetime.strptime(date1, "%Y-%m-%d")
        d2 = datetime.strptime(date2, "%Y-%m-%d")

        difference = abs((d1 - d2).days)

        if difference == 0:
            return 100.0
        elif difference == 1:
            return 80.0
        elif difference == 2:
            return 60.0
        elif difference == 3:
            return 40.0
        elif difference <= 7:
            return 20.0
        else:
            return 0.0

    except ValueError:
        return 0.0