from pathlib import Path
import json
import pandas as pd


STAGED_DATA_PATH = Path("data/staged/data.csv")
VALIDATION_REPORT_PATH = Path("reports/validation_report.json")

EXPECTED_COLUMNS = [
    "gender",
    "height",
    "weight",
    "ap_hi",
    "ap_lo",
    "cholesterol",
    "gluc",
    "smoke",
    "alco",
    "active",
    "cardio",
    "age_years",
]


def main() -> None:
    print(f"Reading staged data from: {STAGED_DATA_PATH}")
    df = pd.read_csv(STAGED_DATA_PATH)

    missing_columns = [col for col in EXPECTED_COLUMNS if col not in df.columns]
    extra_columns = [col for col in df.columns if col not in EXPECTED_COLUMNS]

    missing_values = df.isnull().sum().to_dict()

    report = {
        "row_count": int(len(df)),
        "column_count": int(len(df.columns)),
        "missing_columns": missing_columns,
        "extra_columns": extra_columns,
        "missing_values_by_column": missing_values,
        "checks": {
            "schema_valid": len(missing_columns) == 0 and len(extra_columns) == 0,
            "no_missing_values": int(df.isnull().sum().sum()) == 0,
            "age_years_positive": bool((df["age_years"] > 0).all()),
            "height_positive": bool((df["height"] > 0).all()),
            "weight_positive": bool((df["weight"] > 0).all()),
            "ap_hi_positive": bool((df["ap_hi"] > 0).all()),
            "ap_lo_positive": bool((df["ap_lo"] > 0).all()),
        },
    }

    VALIDATION_REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(VALIDATION_REPORT_PATH, "w") as f:
        json.dump(report, f, indent=4)

    print(f"Validation report saved to: {VALIDATION_REPORT_PATH}")
    print(json.dumps(report, indent=4))


if __name__ == "__main__":
    main()