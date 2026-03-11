import unittest
import csv
from datetime import datetime


class CSVTestResult(unittest.TextTestResult):
    def __init__(self, stream, descriptions, verbosity):
        super().__init__(stream, descriptions, verbosity)
        self.results = []

    def addSuccess(self, test):
        super().addSuccess(test)
        self.results.append((str(test), "PASS"))

    def addFailure(self, test, err):
        super().addFailure(test, err)
        self.results.append((str(test), "FAIL"))

    def addError(self, test, err):
        super().addError(test, err)
        self.results.append((str(test), "ERROR"))


def run_tests():
    loader = unittest.TestLoader()
    suite = loader.discover(".")

    runner = unittest.TextTestRunner(resultclass=CSVTestResult, verbosity=2)
    result = runner.run(suite)

    with open("test_results.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)

        writer.writerow(["timestamp", "test_name", "result"])

        for test, status in result.results:
            writer.writerow([datetime.now(), test, status])

    print("\nTest results written to test_results.csv")


if __name__ == "__main__":
    run_tests()