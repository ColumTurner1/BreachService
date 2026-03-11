import unittest
from src.breach_service import BreachService


class DummyCore:
    api_base_url = ""
    api_key = ""
    timeout = 10
    logger = None
    retry_attempts = 3
    retry_backoff = 2


class TestEmailValidation(unittest.TestCase):

    def setUp(self):
        self.service = BreachService(DummyCore())

    def test_valid_email(self):
        self.assertTrue(self.service.validate_email("test@example.com"))

    def test_invalid_email(self):
        self.assertFalse(self.service.validate_email("invalid-email"))

    def test_invalid_email_missing_domain(self):
        self.assertFalse(self.service.validate_email("test@"))

    def test_invalid_email_missing_at_symbol(self):
        self.assertFalse(self.service.validate_email("testexample.com"))


if __name__ == "__main__":
    unittest.main()