from pathlib import Path
import json
import joblib
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score


STAGED_DATA_PATH = Path("data/staged/data.csv")
MODEL_PATH = Path("models/model.pkl")
EVALUATION_REPORT_PATH = Path("reports/evaluation_report.json")


def clean_bp_values(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df = df[(df["ap_hi"] > 0) & (df["ap_lo"] > 0)]
    df = df[(df["ap_hi"] < 250) & (df["ap_lo"] < 200)]
    return df


def compute_metrics(y_true, y_pred) -> dict:
    return {
        "accuracy": accuracy_score(y_true, y_pred),
        "precision": precision_score(y_true, y_pred),
        "recall": recall_score(y_true, y_pred),
        "f1": f1_score(y_true, y_pred),
    }


def subgroup_metrics(df_subset: pd.DataFrame, model) -> dict:
    if len(df_subset) == 0:
        return {"count": 0}

    x = df_subset.drop(columns=["cardio"])
    y = df_subset["cardio"]
    preds = model.predict(x)

    metrics = compute_metrics(y, preds)
    metrics["count"] = int(len(df_subset))
    return metrics


def main() -> None:
    print(f"Reading staged data from: {STAGED_DATA_PATH}")
    df = pd.read_csv(STAGED_DATA_PATH)

    df = clean_bp_values(df)

    print(f"Loading model from: {MODEL_PATH}")
    model = joblib.load(MODEL_PATH)

    x = df.drop(columns=["cardio"])
    y = df["cardio"]

    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=0.2, random_state=42, stratify=y
    )

    preds = model.predict(x_test)

    overall_metrics = compute_metrics(y_test, preds)

    test_df = x_test.copy()
    test_df["cardio"] = y_test.values

    gender_1_df = test_df[test_df["gender"] == 1]
    gender_2_df = test_df[test_df["gender"] == 2]

    report = {
        "test_size": int(len(x_test)),
        "overall_metrics": overall_metrics,
        "fairness_by_gender": {
            "gender_1": subgroup_metrics(gender_1_df, model),
            "gender_2": subgroup_metrics(gender_2_df, model),
        },
    }

    EVALUATION_REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(EVALUATION_REPORT_PATH, "w") as f:
        json.dump(report, f, indent=4)

    print(f"Saved evaluation report to: {EVALUATION_REPORT_PATH}")
    print(json.dumps(report, indent=4))


if __name__ == "__main__":
    main()