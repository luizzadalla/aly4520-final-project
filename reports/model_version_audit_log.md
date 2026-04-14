# Model Version Audit Log

## Version v1
- Model type: Random Forest Classifier
- Dataset: cardio_train.csv
- Rows before cleaning: 70000
- Rows after blood pressure cleaning: 68985
- Accuracy: 0.7295
- Precision: 0.7524
- Recall: 0.6759
- F1 score: 0.7121
- Fairness check: evaluated by gender subgroup
- Deployment target: SageMaker endpoint `cardio-mlops-endpoint`
- Status: Approved for deployment

## Approval Workflow
1. Run DVC pipeline
2. Review validation report
3. Review evaluation report
4. Review fairness metrics
5. Deploy only if metrics are acceptable

## Audit Notes
- Invalid blood pressure values were detected in raw/staged data
- Random Forest outperformed Logistic Regression baseline
- Small subgroup performance gap observed between gender groups