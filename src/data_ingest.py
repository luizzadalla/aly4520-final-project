from pathlib import Path
import pandas as pd


RAW_DATA_PATH = Path("data/raw/cardio_train.csv")
STAGED_DATA_PATH = Path("data/staged/data.csv")


def main() -> None:
    print(f"Reading raw data from: {RAW_DATA_PATH}")
    df = pd.read_csv(RAW_DATA_PATH, sep=";")

    print(f"Raw shape: {df.shape}")
    print(f"Raw columns: {list(df.columns)}")

    if "id" in df.columns:
        df = df.drop(columns=["id"])

    # Convert age from days to years
    df["age_years"] = (df["age"] / 365.25).round(1)
    df = df.drop(columns=["age"])

    STAGED_DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(STAGED_DATA_PATH, index=False)

    print(f"Saved staged data to: {STAGED_DATA_PATH}")
    print(f"Staged shape: {df.shape}")
    print(f"Staged columns: {list(df.columns)}")


if __name__ == "__main__":
    main()