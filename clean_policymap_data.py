"""
clean_policymap_data.py

Input files expected in the same folder as this script:
- PolicyMap_Data_Average_Travel_Time_To_Work.csv
- PolicyMap_Data_Median_Household_Income.csv
- PolicyMap_Data_Houses_No_Vechile.csv
- PolicyMap_Data_Total_Population.csv

Output:
- cleaned_transportation_capstone_data.csv

This script:
1. Removes the extra PolicyMap header row.
2. Keeps useful columns only.
3. Renames columns to simple names.
4. Converts ZIP codes to 5-digit text.
5. Converts numeric fields to proper numeric data types.
6. Merges all datasets by ZIP code.
7. Removes duplicate ZIP code rows.
8. Saves one clean CSV for Power BI, Excel, or Python modeling.
"""

from pathlib import Path
import pandas as pd


DATA_FILES = {
    "commute": {
        "file": "PolicyMap_Data_Average_Travel_Time_To_Work.csv",
        "value_column": "Avg. Travel Time to Work (in Minutes)",
        "new_column": "avg_commute_minutes",
    },
    "income": {
        "file": "PolicyMap_Data_Median_Household_Income.csv",
        "value_column": "Median Household Income",
        "new_column": "median_household_income",
    },
    "vehicle": {
        "file": "PolicyMap_Data_Houses_No_Vechile.csv",
        "value_column": "Percent Housing Units with 0 Vehicles Available",
        "new_column": "no_vehicle_percent",
    },
    "population": {
        "file": "PolicyMap_Data_Total_Population.csv",
        "value_column": "Population",
        "new_column": "population",
    },
}


def clean_numeric(series: pd.Series) -> pd.Series:
    """Convert PolicyMap number strings into numeric values."""
    return (
        series.astype(str)
        .str.replace(",", "", regex=False)
        .str.replace("$", "", regex=False)
        .str.replace("%", "", regex=False)
        .str.strip()
        .replace({"": pd.NA, "nan": pd.NA, "N/A": pd.NA, "NA": pd.NA})
        .pipe(pd.to_numeric, errors="coerce")
    )


def clean_policymap_file(file_path: Path, value_column: str, new_column: str) -> pd.DataFrame:
    """Clean one PolicyMap CSV and return ZIP code plus one cleaned value column."""
    df = pd.read_csv(file_path)

    # PolicyMap exports include a second header-style row where Geography Name = GeoID_Name.
    df = df[df["Geography Name"].astype(str).str.strip() != "GeoID_Name"].copy()

    keep_columns = ["Geography Name", value_column]
    df = df[keep_columns].copy()

    # Rename columns.
    df = df.rename(
        columns={
            "Geography Name": "zipcode",
            value_column: new_column,
        }
    )

    # Format ZIP code as 5-digit text.
    df["zipcode"] = (
        df["zipcode"]
        .astype(str)
        .str.extract(r"(\d{5})", expand=False)
        .str.zfill(5)
    )

    df[new_column] = clean_numeric(df[new_column])

    # Remove rows without valid ZIP codes and remove duplicate ZIP rows.
    df = df.dropna(subset=["zipcode"])
    df = df.drop_duplicates(subset=["zipcode"], keep="first")

    return df


def main() -> None:
    base_dir = Path(__file__).resolve().parent
    cleaned_tables = []

    for dataset_name, info in DATA_FILES.items():
        file_path = base_dir / info["file"]

        if not file_path.exists():
            raise FileNotFoundError(f"Missing required file: {file_path.name}")

        cleaned = clean_policymap_file(
            file_path=file_path,
            value_column=info["value_column"],
            new_column=info["new_column"],
        )

        print(f"Cleaned {dataset_name}: {cleaned.shape[0]} rows")
        cleaned_tables.append(cleaned)

    # Merge all tables on ZIP code.
    merged = cleaned_tables[0]
    for table in cleaned_tables[1:]:
        merged = merged.merge(table, on="zipcode", how="outer")

    merged = merged.dropna(subset=["avg_commute_minutes"])

    # Sort by ZIP code.
    merged = merged.sort_values("zipcode").reset_index(drop=True)

    output_file = base_dir / "cleaned_transportation_capstone_data.csv"
    merged.to_csv(output_file, index=False)

    print("\nCleaning complete.")
    print(f"Rows in final dataset: {merged.shape[0]}")
    print(f"Columns in final dataset: {list(merged.columns)}")
    print(f"Saved cleaned file to: {output_file}")


if __name__ == "__main__":
    main()
