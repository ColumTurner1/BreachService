import csv
from collections import Counter


def load_results(filename: str) -> list[dict]:
    """
    Load breach screening results from a CSV file.
    """
    with open(filename, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)


def generate_summary(results: list[dict]) -> tuple[int, int, float, Counter]:
    """
    Generate summary statistics from breach results.
    """
    total_emails = len(results)
    breached_count = 0
    breach_sources = []

    for row in results:
        breached_value = row["breached"].strip().lower()

        if breached_value == "true":
            breached_count += 1

            sources = row["site_where_breached"].split(";")
            for source in sources:
                source = source.strip()
                if source:
                    breach_sources.append(source)

    breach_rate = (breached_count / total_emails * 100) if total_emails > 0 else 0.0
    source_counts = Counter(breach_sources)

    return total_emails, breached_count, breach_rate, source_counts


def write_summary_csv(
    filename: str,
    total_emails: int,
    breached_count: int,
    breach_rate: float,
    source_counts: Counter
) -> None:
    """
    Write summary statistics to a CSV file.
    """
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        writer.writerow(["Metric", "Value"])
        writer.writerow(["Total Emails Analysed", total_emails])
        writer.writerow(["Breached Emails", breached_count])
        writer.writerow(["Breach Rate (%)", f"{breach_rate:.2f}"])
        writer.writerow([])
        writer.writerow(["Top Breach Sources", "Count"])

        for source, count in source_counts.most_common():
            writer.writerow([source, count])


def write_summary_markdown(
    filename: str,
    total_emails: int,
    breached_count: int,
    breach_rate: float,
    source_counts: Counter
) -> None:
    """
    Write summary statistics to a Markdown report.
    """
    with open(filename, "w", encoding="utf-8") as f:
        f.write("# Breach Summary Report\n\n")
        f.write("## Overview\n\n")
        f.write(f"- **Total Emails Analysed:** {total_emails}\n")
        f.write(f"- **Breached Emails:** {breached_count}\n")
        f.write(f"- **Breach Rate:** {breach_rate:.2f}%\n\n")

        f.write("## Top Breach Sources\n\n")

        if source_counts:
            for source, count in source_counts.most_common():
                f.write(f"- **{source}**: {count}\n")
        else:
            f.write("No breach sources identified.\n")


def main() -> None:
    input_file = "output_result.csv"
    summary_csv = "breach_summary.csv"
    summary_md = "breach_summary.md"

    results = load_results(input_file)
    total_emails, breached_count, breach_rate, source_counts = generate_summary(results)

    write_summary_csv(summary_csv, total_emails, breached_count, breach_rate, source_counts)
    write_summary_markdown(summary_md, total_emails, breached_count, breach_rate, source_counts)

    print(f"Summary CSV written to: {summary_csv}")
    print(f"Summary Markdown written to: {summary_md}")


if __name__ == "__main__":
    main()