from src.core import Core
from src.breach_service import BreachService
from src.csv_handler import read_emails, write_results


def main():

    core = Core()
    logger = core.logger

    logger.info("Starting breach screening process.")

    service = BreachService(core)

    emails = read_emails("email_list.csv")
    results = []

    for email in emails:
        try:
            result = service.check_email(email)
            results.append(result)
            logger.info(f"Processed: {email}")
        except Exception as e:
            logger.error(f"Failed to process: {email} | Error: {e}")

    write_results("output_result.csv", results)

    logger.info("Breach screening completed.")


if __name__ == "__main__":
    main()