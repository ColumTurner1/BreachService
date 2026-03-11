import unittest
from src.breach_service import BreachService


class DummyCore:
    api_base_url = ""
    api_key = ""
    timeout = 10
    logger = None
    retry_attempts = 3
    retry_backoff = 2


class TestParser(unittest.TestCase):

    def setUp(self):
        self.service = BreachService(DummyCore())

    def test_parse_response(self):
        sample_api_response = {
            "records": [
                {"name": "Example Breach"},
                {"name": "Another Breach"}
            ]
        }

        result = self.service.parse_response(sample_api_response)
        self.assertEqual(len(result), 2)
        self.assertIn("Example Breach", result)
        self.assertIn("Another Breach", result)

    def test_parse_empty_response(self):
        sample_api_response = {}

        result = self.service.parse_response(sample_api_response)
        self.assertEqual(result, [])

    def test_parse_response_deduplicates_names(self):
        sample_api_response = {
            "records": [
                {"name": "Example Breach"},
                {"name": "Example Breach"}
            ]
        }

        result = self.service.parse_response(sample_api_response)
        self.assertEqual(len(result), 1)
        self.assertIn("Example Breach", result)


if __name__ == "__main__":
    unittest.main()