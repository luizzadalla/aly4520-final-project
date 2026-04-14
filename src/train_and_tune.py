from pathlib import Path
import json
import joblib
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier


STAGED_DATA_PATH = Path("data/staged/data.csv")
MODEL_PATH = Path("models/model.pkl")
TRAIN_RESULTS_PATH = Path("models/train_results.json")


def clean_bp_values(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # Keep only rows with realistic positive blood pressure values
    df = df[(df["ap_hi"] > 0) & (df["ap_lo"] > 0)]

    # Optional simple upper/lower sanity bounds
    df = df[(df["ap_hi"] < 250) & (df["ap_lo"] < 200)]

    return df


def evaluate_model(model, x_train, x_test, y_train, y_test) -> dict:
    model.fit(x_train, y_train)
    preds = model.predict(x_test)

    return {
        "accuracy": accuracy_score(y_test, preds),
        "precision": precision_score(y_test, preds),
        "recall": recall_score(y_test, preds),
        "f1": f1_score(y_test, preds),
    }


def main() -> None:
    print(f"Reading staged data from: {STAGED_DATA_PATH}")
    df = pd.read_csv(STAGED_DATA_PATH)

    original_rows = len(df)
    df = clean_bp_values(df)
    cleaned_rows = len(df)

    print(f"Rows before blood pressure cleaning: {original_rows}")
    print(f"Rows after blood pressure cleaning: {cleaned_rows}")

    x = df.drop(columns=["cardio"])
    y = df["cardio"]

    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=0.2, random_state=42, stratify=y
    )

    logistic_model = LogisticRegression(max_iter=1000, random_state=42)
    rf_model = RandomForestClassifier(
        n_estimators=100,
        max_depth=10,
        random_state=42,
        n_jobs=-1
    )

    print("Training Logistic Regression...")
    logistic_metrics = evaluate_model(logistic_model, x_train, x_test, y_train, y_test)

    print("Training Random Forest...")
    rf_metrics = evaluate_model(rf_model, x_train, x_test, y_train, y_test)

    results = {
        "rows_before_cleaning": original_rows,
        "rows_after_cleaning": cleaned_rows,
        "logistic_regression": logistic_metrics,
        "random_forest": rf_metrics,
    }

    if rf_metrics["f1"] >= logistic_metrics["f1"]:
        best_model = rf_model
        best_model_name = "random_forest"
        best_metrics = rf_metrics
    else:
        best_model = logistic_model
        best_model_name = "logistic_regression"
        best_metrics = logistic_metrics

    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(best_model, MODEL_PATH)

    results["best_model"] = best_model_name
    results["best_model_metrics"] = best_metrics

    with open(TRAIN_RESULTS_PATH, "w") as f:
        json.dump(results, f, indent=4)

    print(f"Best model: {best_model_name}")
    print(f"Saved model to: {MODEL_PATH}")
    print(f"Saved training results to: {TRAIN_RESULTS_PATH}")
    print(json.dumps(results, indent=4))


if __name__ == "__main__":
    main()