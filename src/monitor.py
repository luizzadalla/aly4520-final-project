import json

EVAL_PATH = "reports/evaluation_report.json"


def check_drift():
    with open(EVAL_PATH, "r") as f:
        report = json.load(f)

    acc = report["overall_metrics"]["accuracy"]

    print(f"Current accuracy: {acc:.4f}")

    # Simple drift rule
    if acc < 0.70:
        print("ALERT: Model accuracy dropped below threshold!")
    else:
        print("Model performance is stable.")


if __name__ == "__main__":
    check_drift()