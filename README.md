# CSV Data Organizer Tool

A beginner-friendly Python project that organizes business CSV datasets and generates simple reports without using pandas.

## Project Overview

This project simulates a basic office data operator workflow. It reads CSV files, cleans records, removes duplicate rows, counts important categories, calculates totals, searches employee records, and creates summary reports.

The project is based on business-style datasets exported from Excel:

- Employee records
- Weekly export records
- Daily production records

## Technologies Used

- Python
- CSV files
- File handling
- Dictionaries
- Lists
- Loops
- Functions
- GitHub

No pandas or advanced data libraries are used.

## Features

- Read employee, export, and production CSV files
- Clean extra spaces from data
- Remove duplicate rows
- Search employees by name, country, or job type
- Count employees by country
- Count employees by job type
- Calculate export quantity by country
- Calculate production totals by filtration station and well
- Generate cleaned CSV files
- Generate a text-based summary report

## Folder Structure

```text
csv-data-organizer/
|
|-- datasets/
|   |-- employees.csv
|   |-- weekly_exports.csv
|   |-- daily_production.csv
|
|-- reports/
|   |-- cleaned_employees.csv
|   |-- cleaned_weekly_exports.csv
|   |-- cleaned_daily_production.csv
|   |-- summary_report.txt
|
|-- screenshots/
|   |-- terminal_output.png
|
|-- main.py
|-- requirements.txt
|-- README.md
```

## How to Run

1. Download or clone this repository.
2. Open the project folder in VS Code or any code editor.
3. Run the program:

```bash
python main.py
```

4. Choose an option from the menu:

```text
1. Show business summary
2. Search employees
3. Generate clean CSV files and summary report
4. Exit
```

## Example Output

```text
CSV Data Organizer Tool
1. Show business summary
2. Search employees
3. Generate clean CSV files and summary report
4. Exit
```

## What I Learned

Through this project, I practiced:

- Reading and writing CSV files in Python
- Organizing real business-style datasets
- Using functions to structure a program
- Using dictionaries and lists for data processing
- Creating simple reports from raw data
- Building a clean GitHub project for portfolio use

## CV Line

Developed a Python-based CSV data organizer for managing employee, export, and production datasets, including search, cleaning, summary reporting, and structured file output.
