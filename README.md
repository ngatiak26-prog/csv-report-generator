# CSV Report Generator

A Python tool that takes a messy business CSV (sales, inventory, production data) and automatically produces:
- A cleaned CSV file
- A summary chart (bar chart of totals by category + trend line over time)
- A polished PDF report with a summary table and chart, ready to hand to a client

Built for freelance data-cleaning work — designed to be handed a client's raw export and return something they can actually use.

## What it does

1. **Loads** a raw CSV file
2. **Cleans** it — removes blank rows, drops duplicates, strips whitespace, fills missing numeric values
3. **Summarizes** totals by category
4. **Charts** the summary (bar chart) alongside a trend line over time
5. **Generates a PDF report** with a cover section, summary table, and chart — client-ready

## How to use

1. Place your CSV file in the same folder as `main.py`
2. Update the config section at the top of `main.py` to match your data:
   ```python
   INPUT_FILE = "your_file.csv"
   GROUP_COLUMN = "Category"      # column to group totals by
   VALUE_COLUMN = "Amount"        # numeric column to sum
   DATE_COLUMN = "Date"           # column for the trend line (or None to skip)
   CLIENT_NAME = "Client Name"    # shown on the report cover
   ```
3. Run the script
4. Collect the outputs: `cleaned_data.csv`, `summary_chart.png`, `report.pdf`

## Requirements

- pandas
- matplotlib
- reportlab

## Example

`sales_data_sample.csv` is included as a test file — run the script against it out of the box to see the expected output.

## About

Built by Kelvin, an industrial chemistry student combining chemistry with Python/data analysis skills. Part of a growing portfolio applying data tools to real business problems.

