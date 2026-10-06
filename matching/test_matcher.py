from matcher import match_items


def run_test(name, lost_item, found_item):
    result = match_items(lost_item, found_item)

    print(f"\n{name}")
    print("-" * 40)
    print(f"Score: {result['score']}%")
    print(f"Label: {result['label']}")
    print(f"Breakdown: {result['breakdown']}")


# TEST 1: Very similar items
lost_1 = {
    "category": "electronics",
    "description": "Black Lenovo laptop bag with blue keychain",
    "location": "Library",
    "date": "2026-10-05"
}

found_1 = {
    "category": "electronics",
    "description": "Black Lenovo laptop bag with blue keychain",
    "location": "Library",
    "date": "2026-10-05"
}

run_test("TEST 1 - Strong Match", lost_1, found_1)


# TEST 2: Different items
lost_2 = {
    "category": "electronics",
    "description": "Black Lenovo laptop bag",
    "location": "Library",
    "date": "2026-10-05"
}

found_2 = {
    "category": "clothing",
    "description": "Red cotton jacket",
    "location": "Canteen",
    "date": "2026-10-08"
}

run_test("TEST 2 - Unrelated Items", lost_2, found_2)


# TEST 3: Same item but different location
lost_3 = {
    "category": "electronics",
    "description": "Black Lenovo laptop bag",
    "location": "Library",
    "date": "2026-10-05"
}

found_3 = {
    "category": "electronics",
    "description": "Black Lenovo laptop bag",
    "location": "Canteen",
    "date": "2026-10-05"
}

run_test("TEST 3 - Same Item, Different Location", lost_3, found_3)


# TEST 4: Same category, somewhat similar description
lost_4 = {
    "category": "electronics",
    "description": "Black wireless earbuds",
    "location": "Library",
    "date": "2026-10-05"
}

found_4 = {
    "category": "electronics",
    "description": "Black Bluetooth earphones",
    "location": "Library",
    "date": "2026-10-06"
}

run_test("TEST 4 - Possible Match", lost_4, found_4)


# TEST 5: Missing description
lost_5 = {
    "category": "electronics",
    "description": "",
    "location": "Library",
    "date": "2026-10-05"
}

found_5 = {
    "category": "electronics",
    "description": "Black phone",
    "location": "Library",
    "date": "2026-10-05"
}

run_test("TEST 5 - Missing Description", lost_5, found_5)