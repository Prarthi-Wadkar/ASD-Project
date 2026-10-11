
import unittest

from matcher import match_items


class TestMatcher(unittest.TestCase):

    def setUp(self):
        self.lost = {
            "id": 101,
            "category": "electronics",
            "description": "Black Lenovo laptop bag with blue keychain",
            "location": "Library",
            "date": "2026-10-05"
        }

        self.found = {
            "id": 201,
            "category": "electronics",
            "description": "Black Lenovo laptop bag with blue keychain",
            "location": "Library",
            "date": "2026-10-05"
        }

    def test_strong_match(self):
        result = match_items(self.lost, self.found)

        self.assertEqual(result["score"], 100.0)
        self.assertEqual(result["label"], "High Match")

    def test_unrelated_items(self):
        lost = {
            "category": "electronics",
            "description": "Black Lenovo laptop bag",
            "location": "Library",
            "date": "2026-10-05"
        }
        found = {
            "category": "clothing",
            "description": "Red cotton jacket",
            "location": "Canteen",
            "date": "2026-10-08"
        }

        result = match_items(lost, found)

        self.assertLess(result["score"], 60)
        self.assertEqual(result["label"], "Low Match")

    def test_same_item_different_location(self):
        found = {
            **self.lost,
            "location": "Canteen"
        }

        result = match_items(self.lost, found)

        self.assertGreaterEqual(result["score"], 80)
        self.assertEqual(result["label"], "High Match")

    def test_possible_match(self):
        lost = {
            "category": "electronics",
            "description": "Black wireless earbuds",
            "location": "Library",
            "date": "2026-10-05"
        }
        found = {
            "category": "electronics",
            "description": "Black Bluetooth earphones",
            "location": "Library",
            "date": "2026-10-06"
        }

        result = match_items(lost, found)

        self.assertGreaterEqual(result["score"], 60)
        self.assertLess(result["score"], 80)
        self.assertEqual(result["label"], "Possible Match")

    def test_missing_description(self):
        lost = {
            "category": "electronics",
            "description": "",
            "location": "Library",
            "date": "2026-10-05"
        }
        found = {
            "category": "electronics",
            "description": "Black phone",
            "location": "Library",
            "date": "2026-10-05"
        }

        result = match_items(lost, found)

        self.assertEqual(result["score"], 60.0)
        self.assertEqual(result["label"], "Possible Match")

    def test_result_contains_score_breakdown(self):
        result = match_items(self.lost, self.found)

        self.assertIn("score", result)
        self.assertIn("label", result)
        self.assertIn("breakdown", result)

        for component in ("description", "category", "location", "date"):
            self.assertIn(component, result["breakdown"])


if __name__ == "__main__":
    unittest.main()
