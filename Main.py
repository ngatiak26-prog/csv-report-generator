"""
CSV Cleaning + Report Generator Template
-----------------------------------------
A reusable starter script for freelance data-cleaning gigs.

HOW TO USE ON REPLIT:
1. Create a new Python Repl.
2. Upload the client's CSV file (drag into the Files panel, or use the
   upload button). Update INPUT_FILE below to match its name.
3. Click Run. It will:
   - Clean the data (remove blanks, fix column names, drop duplicates)
   - Print a quick summary
   - Save a cleaned CSV
   - Save a chart image (bar chart of totals by category)
4. Download the output files from the Files panel and send to the client.

Customize the CLEANING and REPORT sections per client — this is just
a solid starting skeleton.
"""

import pandas as pd
import matplotlib
matplotlib.use("Agg")  # non-interactive backend, needed for cloud/headless environments like Replit
import matplotlib.pyplot as plt
from datetime import date
from reportlab.lib.pagesizes import letter
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
)
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

# ---------- CONFIG (edit these per client) ----------
INPUT_FILE = "sales_data.csv"       # the client's raw file
OUTPUT_CSV = "cleaned_data.csv"     # cleaned file to send back
OUTPUT_CHART = "summary_chart.png"  # chart image to send back
OUTPUT_PDF = "report.pdf"           # polished PDF report to send back
CLIENT_NAME = "Client Name"         # shown on the report cover
GROUP_COLUMN = "Category"           # column to group/summarize by
VALUE_COLUMN = "Amount"             # numeric column to sum/analyze
DATE_COLUMN = "Date"                # column to use for the trend line (set to None to skip)
# ------------------------------------------------------


def load_data(path):
    df = pd.read_csv(path)
    print(f"Loaded {len(df)} rows, {len(df.columns)} columns.")
    print("Columns found:", list(df.columns))
    return df


def clean_data(df):
    # Standardize column names: strip spaces, lowercase-safe
    df.columns = [c.strip() for c in df.columns]

    # Drop fully empty rows
    df = df.dropna(how="all")

    # Drop exact duplicate rows
    before = len(df)
    df = df.drop_duplicates()
    print(f"Removed {before - len(df)} duplicate rows.")

    # Strip whitespace from text columns
    for col in df.select_dtypes(include="object").columns:
        df[col] = df[col].astype(str).str.strip()

    # Fill missing numeric values with 0 (adjust as needed per client)
    numeric_cols = df.select_dtypes(include="number").columns
    df[numeric_cols] = df[numeric_cols].fillna(0)

    return df


def generate_summary(df):
    if GROUP_COLUMN in df.columns and VALUE_COLUMN in df.columns:
        summary = df.groupby(GROUP_COLUMN)[VALUE_COLUMN].sum().sort_values(ascending=False)
        print("\n--- Summary ---")
        print(summary)
        return summary
    else:
        print(f"\nSkipping summary: '{GROUP_COLUMN}' or '{VALUE_COLUMN}' not found in columns.")
        return None


def make_chart(df, summary):
    if summary is None or summary.empty:
        return

    # Decide layout: 2 charts side by side if we have a usable date column,
    # otherwise just the 1 bar chart.
    has_trend = DATE_COLUMN and DATE_COLUMN in df.columns

    if has_trend:
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    else:
        fig, ax1 = plt.subplots(figsize=(8, 5))

    # --- Bar chart: totals by category ---
    summary.plot(kind="bar", color="#4C72B0", ax=ax1)
    ax1.set_title(f"Total {VALUE_COLUMN} by {GROUP_COLUMN}")
    ax1.set_ylabel(VALUE_COLUMN)
    ax1.set_xlabel(GROUP_COLUMN)

    # --- Line chart: trend over time ---
    if has_trend:
        df_trend = df.copy()
        df_trend[DATE_COLUMN] = pd.to_datetime(df_trend[DATE_COLUMN], errors="coerce")
        df_trend = df_trend.dropna(subset=[DATE_COLUMN])
        daily = df_trend.groupby(DATE_COLUMN)[VALUE_COLUMN].sum().sort_index()

        if not daily.empty:
            ax2.plot(daily.index, daily.values, marker="o", color="#DD8452")
            ax2.set_title(f"{VALUE_COLUMN} Over Time")
            ax2.set_ylabel(VALUE_COLUMN)
            ax2.set_xlabel(DATE_COLUMN)
            ax2.tick_params(axis="x", rotation=45)
        else:
            ax2.axis("off")
            ax2.set_title(f"No valid dates found in '{DATE_COLUMN}'")

    plt.tight_layout()
    plt.savefig(OUTPUT_CHART)
    plt.close(fig)
    print(f"\nChart saved as {OUTPUT_CHART}")


def make_pdf_report(df, summary):
    styles = getSampleStyleSheet()
    story = []

    # --- Cover / header ---
    story.append(Paragraph("Data Report", styles["Title"]))
    story.append(Paragraph(f"Prepared for: {CLIENT_NAME}", styles["Normal"]))
    story.append(Paragraph(f"Date: {date.today().strftime('%d %B %Y')}", styles["Normal"]))
    story.append(Spacer(1, 20))

    # --- Overview ---
    story.append(Paragraph("Overview", styles["Heading2"]))
    story.append(Paragraph(
        f"This report covers {len(df)} records after cleaning. "
        f"Duplicate rows and blank entries were removed, and totals were "
        f"summarized by {GROUP_COLUMN}.",
        styles["Normal"]
    ))
    story.append(Spacer(1, 16))

    # --- Summary table ---
    if summary is not None and not summary.empty:
        story.append(Paragraph(f"Summary: Total {VALUE_COLUMN} by {GROUP_COLUMN}", styles["Heading2"]))
        table_data = [[GROUP_COLUMN, VALUE_COLUMN]] + [
            [str(idx), f"{val:,.2f}"] for idx, val in summary.items()
        ]
        table = Table(table_data, hAlign="LEFT")
        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#4C72B0")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F2F2F2")]),
            ("FONTSIZE", (0, 0), (-1, -1), 9),
            ("TOPPADDING", (0, 0), (-1, -1), 4),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ]))
        story.append(table)
        story.append(Spacer(1, 20))

        # --- Chart ---
        story.append(Paragraph("Chart", styles["Heading2"]))
        story.append(Image(OUTPUT_CHART, width=480, height=200))

    doc = SimpleDocTemplate(OUTPUT_PDF, pagesize=letter)
    doc.build(story)
    print(f"PDF report saved as {OUTPUT_PDF}")


def main():
    df = load_data(INPUT_FILE)
    df_clean = clean_data(df)
    df_clean.to_csv(OUTPUT_CSV, index=False)
    print(f"Cleaned data saved as {OUTPUT_CSV}")

    summary = generate_summary(df_clean)
    make_chart(df_clean, summary)
    make_pdf_report(df_clean, summary)

    print("\nDone. Send the client:")
    print(f"  1. {OUTPUT_PDF}  <- the polished report (this is usually all they need)")
    print(f"  2. {OUTPUT_CSV}  <- cleaned raw data, optional")


if __name__ == "__main__":
    main()
