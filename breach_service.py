import re
import requests
from dataclasses import dataclass
from typing import List
from tenacity import retry, stop_after_attempt, wait_exponential

EMAIL_REGEX = r"^[\w\.-]+@[\w\.-]+\.\w+$"


@dataclass
class BreachResult:
    email_address: str
    breached: bool
    site_where_breached: List[str]


class BreachService:
    """
    Handles all breach intelligence API interactions.
    """

    def __init__(self, core):
        self.base_url = core.api_base_url
        self.api_key = core.api_key
        self.timeout = core.timeout
        self.logger = core.logger
        self.retry_attempts = core.retry_attempts
        self.retry_backoff = core.retry_backoff

    def validate_email(self, email: str) -> bool:
        return re.match(EMAIL_REGEX, email) is not None

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=2), reraise=True)
    def check_email(self, email: str) -> BreachResult:
        """
        Check a single email using IntelX intelligent search (2-step process).
        """

        if not self.validate_email(email):
            self.logger.error(f"Invalid email format: {email}")
            return BreachResult(email, False, [])

        search_url = f"{self.base_url}/intelligent/search"
        headers = {"x-key": self.api_key}
        payload = {"term": email}

        try:
            # STEP 1 — Start search
            response = requests.post(
                search_url,
                headers=headers,
                json=payload,
                timeout=self.timeout
            )

            self.logger.debug(f"POST {search_url} | Status Code: {response.status_code}")
            response.raise_for_status()

            data = response.json()
            self.logger.debug(f"Initial search response for {email}: {data}")

            search_id = data.get("id")

            if not search_id:
                self.logger.warning(f"No search ID returned for {email}")
                return BreachResult(email, False, [])

            # STEP 2 — Retrieve results
            result_url = f"{self.base_url}/intelligent/search/result"
            params = {"id": search_id}

            result_response = requests.get(
                result_url,
                headers=headers,
                params=params,
                timeout=self.timeout
            )

            self.logger.debug(f"GET {result_url} | Status Code: {result_response.status_code}")
            result_response.raise_for_status()

            result_data = result_response.json()
            self.logger.debug(f"Search results for {email}: {result_data}")

            breaches = self.parse_response(result_data)

            self.logger.debug(f"Parsed breaches for {email}: {breaches}")

            return BreachResult(
                email_address=email,
                breached=len(breaches) > 0,
                site_where_breached=breaches
            )

        except requests.RequestException as e:
            self.logger.error(f"API error for {email}: {e}")
            raise

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=2), reraise=True)
    def check_email_get(self, email: str) -> BreachResult:
        """
        Check a single email using GET request instead of POST.
        """

        if not self.validate_email(email):
            self.logger.error(f"Invalid email format: {email}")
            return BreachResult(email, False, [])

        url = f"{self.base_url}/intelligent/search"
        headers = {"x-key": self.api_key}
        params = {"term": email}

        try:
            response = requests.get(
                url,
                headers=headers,
                params=params,
                timeout=self.timeout
            )

            self.logger.debug(f"GET {url} | Status Code: {response.status_code}")

            if response.status_code == 429:
                self.logger.warning("Rate limit exceeded (429). Retrying...")
                response.raise_for_status()

            response.raise_for_status()

            data = response.json()
            self.logger.debug(f"Raw API response for {email}: {data}")

            breaches = self.parse_response(data)
            self.logger.debug(f"Parsed breaches for {email}: {breaches}")

            return BreachResult(
                email_address=email,
                breached=len(breaches) > 0,
                site_where_breached=breaches
            )

        except requests.RequestException as e:
            self.logger.error(f"API GET error for {email}: {e}")
            raise


    def _clean_breach_name(self, name: str) -> str:
        """
        Convert IntelX dataset filenames into readable breach names.
        """

        if not name:
            return name

        # Remove file extensions
        name = name.replace(".csv", "").replace(".zip", "").replace(".txt", "")

        # Remove Parts
        name = re.sub(r"\[Part.*?\]", "", name)

        # Remove Record Numbers
        name = re.sub(r"^\d+\s+million\s+", "", name, flags=re.IGNORECASE)

        # Handle path names
        if "/" in name:
            name = name.split("/")[0]

        # Extract primary dataset name
        if "_" in name:
            name = name.split("_")[0]

        return name.strip()


    def parse_response(self, data: dict) -> list[str]:
        breaches = []

        records = data.get("records", [])

        for record in records:
            name = record.get("name")

            if name:
                clean_name = self._clean_breach_name(name)
                breaches.append(clean_name)

        return list(set(breaches))