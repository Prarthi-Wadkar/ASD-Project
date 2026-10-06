from similarity import (
    text_similarity,
    category_similarity,
    location_similarity,
    date_similarity
)


def calculate_match_score(lost_item, found_item):
    """Calculate weighted similarity score between lost and found items."""

    description_score = text_similarity(
        lost_item.get("description"),
        found_item.get("description")
    )

    category_score = category_similarity(
        lost_item.get("category"),
        found_item.get("category")
    )

    location_score = location_similarity(
        lost_item.get("location"),
        found_item.get("location")
    )

    date_score = date_similarity(
        lost_item.get("date"),
        found_item.get("date")
    )

    final_score = (
        description_score * 0.40 +
        category_score * 0.20 +
        location_score * 0.20 +
        date_score * 0.20
    )

    return round(final_score, 2)


def get_match_label(score):
    """Convert score into a human-readable match label."""

    if score >= 80:
        return "High Match"
    elif score >= 60:
        return "Possible Match"
    else:
        return "Low Match"


def match_items(lost_item, found_item):
    """Compare a lost item and found item and return complete match result."""

    description_score = text_similarity(
        lost_item.get("description"),
        found_item.get("description")
    )

    category_score = category_similarity(
        lost_item.get("category"),
        found_item.get("category")
    )

    location_score = location_similarity(
        lost_item.get("location"),
        found_item.get("location")
    )

    date_score = date_similarity(
        lost_item.get("date"),
        found_item.get("date")
    )

    final_score = round(
        description_score * 0.40 +
        category_score * 0.20 +
        location_score * 0.20 +
        date_score * 0.20,
        2
    )

    return {
        "score": final_score,
        "label": get_match_label(final_score),
        "breakdown": {
            "description": description_score,
            "category": category_score,
            "location": location_score,
            "date": date_score
        }
    }