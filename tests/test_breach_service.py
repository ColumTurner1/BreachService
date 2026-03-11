import unittest
from unittest.mock import patch, Mock
import requests

from src.breach_service import BreachService, BreachResult


class DummyLogger:
    def error(self, msg):
        pass

    def warning(self, msg):
        pass

    def debug(self, msg):
        pass

    def info(self, msg):
        pass


class DummyCore:
    api_base_url = "https://free.intelx.io"
    api_key = "fake-key"
    timeout = 10
    logger = DummyLogger()
    retry_attempts = 3
    retry_backoff = 2


class TestBreachService(unittest.TestCase):

    def setUp(self):
        self.service = BreachService(DummyCore())

    @patch("src.breach_service.requests.post")
    def test_invalid_email_returns_false_without_api_call(self, mock_post):
        result = self.service.check_email("invalid-email")

        self.assertIsInstance(result, BreachResult)
        self.assertFalse(result.breached)
        self.assertEqual(result.site_where_breached, [])
        mock_post.assert_not_called()

    @patch("src.breach_service.requests.get")
    @patch("src.breach_service.requests.post")
    def test_check_email_success_breached_true(self, mock_post, mock_get):
        mock_post_response = Mock()
        mock_post_response.status_code = 200
        mock_post_response.json.return_value = {"id": "search-123"}
        mock_post_response.raise_for_status.return_value = None

        mock_get_response = Mock()
        mock_get_response.status_code = 200
        mock_get_response.json.return_value = {
            "records": [{"name": "Example Breach"}]
        }
        mock_get_response.raise_for_status.return_value = None

        mock_post.return_value = mock_post_response
        mock_get.return_value = mock_get_response

        result = self.service.check_email("test@example.com")

        self.assertTrue(result.breached)
        self.assertIn("Example Breach", result.site_where_breached)

    @patch("src.breach_service.requests.get")
    @patch("src.breach_service.requests.post")
    def test_check_email_success_breached_false_when_no_records(self, mock_post, mock_get):
        mock_post_response = Mock()
        mock_post_response.status_code = 200
        mock_post_response.json.return_value = {"id": "search-123"}
        mock_post_response.raise_for_status.return_value = None

        mock_get_response = Mock()
        mock_get_response.status_code = 200
        mock_get_response.json.return_value = {"records": []}
        mock_get_response.raise_for_status.return_value = None

        mock_post.return_value = mock_post_response
        mock_get.return_value = mock_get_response

        result = self.service.check_email("safe@example.com")

        self.assertFalse(result.breached)
        self.assertEqual(result.site_where_breached, [])

    @patch("src.breach_service.requests.post")
    def test_check_email_429_raises_after_retries(self, mock_post):
        mock_response = Mock()
        mock_response.status_code = 429
        mock_response.raise_for_status.side_effect = requests.HTTPError("429 Too Many Requests")
        mock_post.return_value = mock_response

        with self.assertRaises(requests.HTTPError):
            self.service.check_email("test@example.com")

        self.assertGreaterEqual(mock_post.call_count, 1)

    @patch("src.breach_service.requests.post")
    def test_check_email_network_error_raises(self, mock_post):
        mock_post.side_effect = requests.ConnectionError("Network error")

        with self.assertRaises(requests.ConnectionError):
            self.service.check_email("test@example.com")

        self.assertGreaterEqual(mock_post.call_count, 1)

    @patch("src.breach_service.requests.get")
    @patch("src.breach_service.requests.post")
    def test_check_email_no_search_id_returns_false(self, mock_post, mock_get):
        mock_post_response = Mock()
        mock_post_response.status_code = 200
        mock_post_response.json.return_value = {}
        mock_post_response.raise_for_status.return_value = None
        mock_post.return_value = mock_post_response

        result = self.service.check_email("test@example.com")

        self.assertFalse(result.breached)
        self.assertEqual(result.site_where_breached, [])
        mock_get.assert_not_called()


if __name__ == "__main__":
    unittest.main()