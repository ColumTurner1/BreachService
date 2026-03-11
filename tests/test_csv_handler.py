import unittest
import os
import tempfile
import csv

from src.csv_handler import write_results, read_emails
from src.breach_service import BreachResult


class TestCSVHandler(unittest.TestCase):

    def test_csv_write(self):
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            file_path = tmp.name

        results = [
            BreachResult("test@example.com", False, []),
            BreachResult("breached@test.com", True, ["ExampleBreach"])
        ]

        write_results(file_path, results)

        self.assertTrue(os.path.exists(file_path))

        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        self.assertIn("test@example.com", content)
        self.assertIn("breached@test.com", content)
        self.assertIn("ExampleBreach", content)

        os.remove(file_path)

    def test_read_emails(self):
        with tempfile.NamedTemporaryFile(mode="w", delete=False, newline="", encoding="utf-8") as tmp:
            writer = csv.writer(tmp)
            writer.writerow(["email"])
            writer.writerow(["alice@example.com"])
            writer.writerow(["bob@example.com"])
            file_path = tmp.name

        emails = read_emails(file_path)

        self.assertEqual(len(emails), 2)
        self.assertIn("alice@example.com", emails)
        self.assertIn("bob@example.com", emails)

        os.remove(file_path)

    def test_write_results_creates_header(self):
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            file_path = tmp.name

        results = []
        write_results(file_path, results)

        with open(file_path, "r", encoding="utf-8") as f:
            header = f.readline().strip()

        self.assertEqual(header, "email_address,breached,site_where_breached")

        os.remove(file_path)


if __name__ == "__main__":
    unittest.main()