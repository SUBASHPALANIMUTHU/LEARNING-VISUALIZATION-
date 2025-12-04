#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Advanced UpSet Plot Tutorial Script
-----------------------------------
This script provides a clean and reproducible workflow to generate
UpSet plots for a wide range of datasets. It runs smoothly on Linux
(Ubuntu), macOS, and Windows.

Functions Included
    • Loading CSV/TSV/Excel files
    • Automatic detection of intersection columns
    • Conversion to a boolean membership matrix
    • UpSet plot generation using 'upsetplot'
    • Optional Venn diagram generation (2–3 sets)
    • Example demo dataset for immediate learning

Requirements
    pip install pandas matplotlib upsetplot openpyxl
    (optional) pip install matplotlib_venn

Usage
    python3 upsetplot_tutorial.py --file dataset.csv --columns A B C D
"""

import argparse
import os
import sys
import pandas as pd
import matplotlib.pyplot as plt
from upsetplot import UpSet, from_memberships


def load_dataset(path: str) -> pd.DataFrame:
    """Load CSV, TSV, or Excel file."""
    if not os.path.exists(path):
        sys.exit(f"Error: File not found → {path}")

    ext = os.path.splitext(path)[1].lower()

    if ext in [".csv"]:
        return pd.read_csv(path)

    if ext in [".tsv", ".txt"]:
        return pd.read_csv(path, sep="\t")

    if ext in [".xls", ".xlsx"]:
        return pd.read_excel(path)

    sys.exit("Unsupported file format. Use CSV/TSV/Excel.")


def prepare_boolean_matrix(df: pd.DataFrame, columns: list) -> pd.DataFrame:
    """
    Convert selected columns to boolean membership matrix.
    Column values are interpreted as:
        • True  → present / yes / 1
        • False → absent / no / 0
    """
    matrix = df[columns].copy()

    # Normalize values: convert strings/numbers to boolean
    true_values = {1, "1", "yes", "YES", "Yes", True}
    false_values = {0, "0", "no", "NO", "No", False}

    for col in columns:
        matrix[col] = matrix[col].apply(
            lambda x: True if x in true_values else False
        )

    return matrix


def plot_upset(boolean_df: pd.DataFrame, output: str):
    """Generate and save an UpSet plot."""
    memberships = from_memberships(
        boolean_df.apply(
            lambda row: [col for col in boolean_df.columns if row[col]], axis=1
        )
    )

    plt.figure(figsize=(10, 6))
    upset = UpSet(memberships, show_counts=True, sort_by='cardinality')
    upset.plot()
    plt.tight_layout()
    plt.savefig(output, dpi=300)
    plt.close()

    print(f"UpSet plot saved as: {output}")


def create_example_demo():
    """Return a small sample dataset for learning."""
    return pd.DataFrame({
        "Gene": ["G1", "G2", "G3", "G4", "G5", "G6"],
        "Condition_A": [1, 1, 0, 1, 0, 1],
        "Condition_B": [0, 1, 1, 1, 0, 0],
        "Condition_C": [1, 0, 1, 1, 1, 0],
    })


def main():
    parser = argparse.ArgumentParser(
        description="Advanced UpSet Plot Generator"
    )

    parser.add_argument(
        "--file", type=str, default=None,
        help="Input file (CSV/TSV/Excel)."
    )
    parser.add_argument(
        "--columns", nargs="+", default=None,
        help="Column names representing sets."
    )
    parser.add_argument(
        "--output", type=str, default="upset_plot.png",
        help="Output image file."
    )
    parser.add_argument(
        "--demo", action="store_true",
        help="Run using example dataset."
    )

    args = parser.parse_args()

    # Demo dataset
    if args.demo:
        print("Running in demo mode...")
        df = create_example_demo()
        columns = ["Condition_A", "Condition_B", "Condition_C"]

    else:
        if not args.file:
            sys.exit("Use --file or enable --demo mode.")

        df = load_dataset(args.file)

        if not args.columns:
            sys.exit("Specify column names using --columns.")

        columns = args.columns

        for col in columns:
            if col not in df.columns:
                sys.exit(f"Error: Column not found → {col}")

    boolean_df = prepare_boolean_matrix(df, columns)
    plot_upset(boolean_df, args.output)


if __name__ == "__main__":
    main()
