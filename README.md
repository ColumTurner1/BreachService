# Breach Intelligence Email Screening Tool

## Overview

This project implements a **Python-based breach intelligence screening tool** for Antrim Logistics Company (ALC). The application checks email addresses against known breach intelligence datasets using the **Intelligence X API**.

The system identifies whether an email address appears in publicly available breach data and produces structured outputs suitable for security analysts.

This tool supports ALC’s risk-assessment process by identifying potentially compromised accounts and informing mitigation actions.

---

# Key Features

* CSV input processing
* Email validation using regex
* Breach intelligence API integration (Intelligence X)
* Retry logic with exponential backoff and error re-raising
* Structured logging with configurable log levels
* CSV result generation for analyst review
* Analyst breach summary reporting
* Comprehensive unit testing suite
* Automated test runner with CSV test result export

---

# System Architecture

```
           +---------------+
           | email_list.csv|
           +-------+-------+
                   |
                   v
             +-----+-----+
             |  main.py  |
             +-----+-----+
                   |
                   v
        +----------+-----------+
        |  BreachService       |
        |  (IntelX API Client) |
        +----------+-----------+
                   |
                   v
           +-------+--------+
           | csv_handler.py |
           +-------+--------+
                   |
                   v
          +------------------+
          | output_result.csv|
          +------------------+
```

---

# Project Structure

```
breach-checker/
│
├── main.py
├── core.py
├── breach_service.py
├── csv_handler.py
│
├── config.yaml
├── .env.example
│
├── email_list.csv
├── output_result.csv
│
├── breach_tool.log
├── report_generator.py
│
├── tests/
│   ├── test_email_validation.py
│   ├── test_csv_handler.py
│   ├── test_parser.py
│   ├── test_breach_service.py
│   ├── run_tests.py
│   └── __init__.py
│
├── test_results.csv
├── requirements.txt
└── README.md
```

---

# Setup

## Requirements

Python 3.10+

Install dependencies:

```
pip install -r requirements.txt
```

---

# Configuration

Create a `.env` file:

```
INTELX_API_KEY=your_api_key_here
```

Example configuration file `config.yaml`:

```yaml
api:
  base_url: https://free.intelx.io
  timeout: 10
  rate_limit_per_minute: 50

logging:
  level: INFO
  file: breach_tool.log

retry:
  attempts: 3
  backoff_seconds: 2
```

---

# Running the Application

Run the main script:

```
python main.py
```

The program will:

1. Load emails from `email_list.csv`
2. Query Intelligence X
3. Write results to `output_result.csv`

Example output:

```
email_address,breached,site_where_breached
example@example.com,False,
admin@steel-gamers.ru,True,Whois/2015-12-12.zip
```

---

# Breach Summary Report

Generate an analyst summary:

```
python report_generator.py
```

Outputs:

```
breach_summary.csv
breach_summary.md
```

These files provide counts of breached emails and the most common breach sources.

---

# Testing

The project includes a comprehensive automated test suite implemented using Python’s `unittest` framework.

Tests cover the core functionality of the system including:

* Email validation
* CSV input and output operations
* API response parsing
* Handling of empty or malformed API responses
* Detection of duplicate breach records
* API success responses
* Invalid email handling
* Retry behaviour and error propagation
* Simulated API rate limiting (HTTP 429)
* Simulated network failures

External API behaviour is safely simulated using `unittest.mock` to avoid consuming API credits and to ensure deterministic testing.

### Running the Test Suite

Run all tests using the automated test runner:
python tests/run_tests.py

### Example Output

* test_valid_email ... PASS
* test_invalid_email ... PASS
* test_parse_response ... PASS
* test_csv_write ... PASS

The test runner also exports structured results to:
* test_results.csv

This file provides an auditable record of automated test execution.
---

# Logging

The application implements structured logging to support observability and troubleshooting.

Logs include:

* API request and response activity
* processing status messages
* retry attempts
* error conditions

Logging behaviour is configured through `config.yaml` and supports adjustable verbosity levels.

Example log entry:
* 2026-03-08 19:38:58 | INFO | Processed example@example.com

Logs are written to:
* breach_tool.log

This allows operational monitoring without cluttering terminal output.

---

# Limitations

* The free Intelligence X API tier has strict rate limits.
* Only email identifiers are currently supported.
* Results depend on third-party breach intelligence data availability.
* The tool currently processes requests sequentially rather than asynchronously.

---

# Ethics & Compliance

This project follows ethical data-handling principles:

* Only synthetic test data is included
* API usage follows provider terms of service
* No personal or sensitive information is stored
* API keys are excluded from version control

The tool is intended solely for **authorised security analysis**.

---

# Future Improvements

Possible extensions include:

* asynchronous API requests to improve throughput
* support for additional breach intelligence providers
* containerisation using Docker
* integration with CI/CD pipelines for automated testing
* visual dashboards for breach analytics
* automated alerting when new breaches are detected

---

# Author

Colum Turner
BSc (Hons) Software, Cloud and Application Development
Belfast Metropolitan College
