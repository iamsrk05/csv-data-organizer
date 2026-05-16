import csv
from pathlib import Path
from collections import Counter, defaultdict

BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "datasets"
REPORT_DIR = BASE_DIR / "reports"


def read_csv(filename):
    """Read a CSV file and return a list of dictionaries."""
    path = DATA_DIR / filename
    with open(path, "r", encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)
        return list(reader)


def clean_text(value):
    """Remove extra spaces from text values."""
    return str(value).strip()


def safe_number(value):
    """Convert a value into a number safely."""
    try:
        return float(value)
    except (ValueError, TypeError):
        return 0


def clean_records(records):
    """Clean spaces from every value in every row."""
    cleaned = []
    for row in records:
        clean_row = {}
        for key, value in row.items():
            clean_row[clean_text(key)] = clean_text(value)
        cleaned.append(clean_row)
    return cleaned


def remove_duplicate_rows(records):
    """Remove exact duplicate rows."""
    unique_records = []
    seen = set()

    for row in records:
        row_tuple = tuple(row.items())
        if row_tuple not in seen:
            unique_records.append(row)
            seen.add(row_tuple)

    return unique_records


def save_clean_csv(filename, records):
    """Save cleaned records into a new CSV file."""
    if not records:
        return

    REPORT_DIR.mkdir(exist_ok=True)
    output_path = REPORT_DIR / filename

    with open(output_path, "w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=records[0].keys())
        writer.writeheader()
        writer.writerows(records)


def count_by_column(records, column_name):
    """Count how many times each value appears in a column."""
    counter = Counter()

    for row in records:
        value = row.get(column_name, "Unknown")
        if value == "":
            value = "Unknown"
        counter[value] += 1

    return counter


def total_by_column(records, group_column, number_column):
    """Add number values by category."""
    totals = defaultdict(float)

    for row in records:
        category = row.get(group_column, "Unknown") or "Unknown"
        amount = safe_number(row.get(number_column, 0))
        totals[category] += amount

    return totals


def write_summary_report(employees, exports, production):
    """Create a simple business summary report as a text file."""
    employee_by_country = count_by_column(employees, "address")
    employee_by_job = count_by_column(employees, "Job_type")
    exports_by_country = total_by_column(exports, "Country", "quantity")
    production_by_station = total_by_column(production, "filterationName", "numberOfDailyBarrel")
    production_by_well = total_by_column(production, "wellName", "numberOfDailyBarrel")

    total_employees = len(employees)
    total_export_quantity = sum(exports_by_country.values())
    total_production = sum(production_by_station.values())

    report_lines = []
    report_lines.append("CSV DATA ORGANIZER - SUMMARY REPORT")
    report_lines.append("=" * 45)
    report_lines.append("")
    report_lines.append(f"Total employees: {total_employees}")
    report_lines.append(f"Total export quantity: {total_export_quantity:,.0f}")
    report_lines.append(f"Total production barrels: {total_production:,.0f}")
    report_lines.append("")

    report_lines.append("Employees by Country")
    report_lines.append("-" * 25)
    for country, count in employee_by_country.most_common():
        report_lines.append(f"{country}: {count}")
    report_lines.append("")

    report_lines.append("Employees by Job Type")
    report_lines.append("-" * 25)
    for job, count in employee_by_job.most_common():
        report_lines.append(f"{job}: {count}")
    report_lines.append("")

    report_lines.append("Export Quantity by Country")
    report_lines.append("-" * 25)
    for country, total in sorted(exports_by_country.items()):
        report_lines.append(f"{country}: {total:,.0f}")
    report_lines.append("")

    report_lines.append("Production by Filtration Station")
    report_lines.append("-" * 35)
    for station, total in sorted(production_by_station.items()):
        report_lines.append(f"{station}: {total:,.0f}")
    report_lines.append("")

    report_lines.append("Production by Well")
    report_lines.append("-" * 20)
    for well, total in sorted(production_by_well.items()):
        report_lines.append(f"{well}: {total:,.0f}")

    output_path = REPORT_DIR / "summary_report.txt"
    with open(output_path, "w", encoding="utf-8") as file:
        file.write("\n".join(report_lines))

    return output_path


def search_employees(employees, keyword):
    """Search employee records by name, country, or job type."""
    keyword = keyword.lower().strip()
    results = []

    for emp in employees:
        full_name = f"{emp.get('firstName', '')} {emp.get('lastName', '')}".lower()
        job = emp.get("Job_type", "").lower()
        country = emp.get("address", "").lower()

        if keyword in full_name or keyword in job or keyword in country:
            results.append(emp)

    return results


def print_menu():
    print("\nCSV Data Organizer Tool")
    print("1. Show business summary")
    print("2. Search employees")
    print("3. Generate clean CSV files and summary report")
    print("4. Exit")


def main():
    employees = remove_duplicate_rows(clean_records(read_csv("employees.csv")))
    exports = remove_duplicate_rows(clean_records(read_csv("weekly_exports.csv")))
    production = remove_duplicate_rows(clean_records(read_csv("daily_production.csv")))

    while True:
        print_menu()
        choice = input("Choose an option: ")

        if choice == "1":
            print("\nBusiness Summary")
            print("-" * 20)
            print(f"Employees loaded: {len(employees)}")
            print(f"Export records loaded: {len(exports)}")
            print(f"Production records loaded: {len(production)}")

            exports_by_country = total_by_column(exports, "Country", "quantity")
            for country, total in sorted(exports_by_country.items()):
                print(f"{country}: {total:,.0f} barrels exported")

        elif choice == "2":
            keyword = input("Search by employee name, country, or job type: ")
            results = search_employees(employees, keyword)

            if not results:
                print("No matching employees found.")
            else:
                print(f"\nFound {len(results)} employee(s):")
                for emp in results[:20]:
                    print(f"ID: {emp.get('id')} | {emp.get('firstName')} {emp.get('lastName')} | {emp.get('Job_type')} | {emp.get('address')}")
                if len(results) > 20:
                    print("Only first 20 results shown.")

        elif choice == "3":
            save_clean_csv("cleaned_employees.csv", employees)
            save_clean_csv("cleaned_weekly_exports.csv", exports)
            save_clean_csv("cleaned_daily_production.csv", production)
            report_path = write_summary_report(employees, exports, production)
            print(f"Reports created successfully in: {REPORT_DIR}")
            print(f"Summary report: {report_path}")

        elif choice == "4":
            print("Goodbye!")
            break

        else:
            print("Invalid option. Please choose 1, 2, 3, or 4.")


if __name__ == "__main__":
    main()
