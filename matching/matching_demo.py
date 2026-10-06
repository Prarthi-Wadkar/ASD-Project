from matcher import match_items


lost_item = {
    "id": 101,
    "category": "electronics",
    "description": "Black Lenovo laptop bag with blue keychain",
    "location": "Library",
    "date": "2026-10-05"
}

found_item = {
    "id": 201,
    "category": "electronics",
    "description": "Black Lenovo laptop bag with blue keychain",
    "location": "Library",
    "date": "2026-10-05"
}


result = match_items(lost_item, found_item)

print(result)