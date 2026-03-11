import csv
from typing import List
from src.breach_service import BreachResult


def read_emails(file_path: str) -> List[str]:
    """
    Reads emails from a CSV file with header: email
    """
    emails = []

    with open(file_path, newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            emails.append(row["email"])

    return emails


def write_results(file_path: str, results: List[BreachResult]) -> None:
    """
    Writes results to output CSV.
    """
    with open(file_path, "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["email_address", "breached", "site_where_breached"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()

        for result in results:
            writer.writerow({
                "email_address": result.email_address,
                "breached": result.breached,
                "site_where_breached": ";".join(result.site_where_breached)
            })
