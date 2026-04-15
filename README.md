End-to-End MLOps Pipeline (Cardiovascular Risk Prediction)

Project Overview
This project implements a full end-to-end MLOps pipeline for predicting cardiovascular disease risk using a structured dataset. The pipeline covers data ingestion, validation, model training, evaluation, deployment, monitoring, and governance. The system is designed to simulate a production-ready ML workflow using modern tools such as DVC, Docker, AWS SageMaker, and GitHub Actions.

Dataset: Cardiovascular dataset (cardio_train.csv)
- Source: Kaggle by Ulianova (2019)
- Size: 70,000 rows
Features include:
- Demographics: age, gender
- Health metrics: height, weight, blood pressure
- Lifestyle: smoking, alcohol, activity
- Target: cardio (presence of cardiovascular disease)

Data is versioned using DVC and stored in AWS S3.

Project Structure
aly4520-final-project/
├── data/

│   ├── raw/

│   └── staged/

├── src/

│   ├── data_ingest.py

│   ├── data_validation.py

│   ├── train_and_tune.py
│   ├── evaluate.py

│   ├── monitor.py

├── inference/

│   ├── inference.py

│   ├── predict.py

├── models/

├── reports/

│   ├── validation_report.json.dvc

│   ├── evaluation_report.json.dvc

│   ├── incident_playbook.md

│   ├── model_version_audit_log.md

├── .github/workflows/

│   ├── ci.yml

│   ├── cd.yml

├── Dockerfile

├── dvc.yaml

├── requirements.txt

└── README.md

Local Execution
1. Install dependencies
pip install -r requirements.txt
pip install dvc[s3]
2. Pull data from DVC
dvc pull
3. Run full pipeline
dvc repro

DVC Pipeline
The pipeline consists of:
- Data ingestion → clean and prepare dataset
- Data validation → schema and quality checks
- Model training → Logistic Regression and Random Forest
- Evaluation → performance + fairness metrics
Artifacts are versioned and stored in S3.



Docker
Build the inference container:
docker build -t cardio-mlops .
Run locally:
docker run -p 8080:8080 cardio-mlops
Test endpoints:

curl http://localhost:8080/ping

curl -X POST http://localhost:8080/invocations \
  -H "Content-Type: application/json" \
  -d '{"gender":1,"height":170,"weight":70,"ap_hi":120,"ap_lo":80,"cholesterol":1,"gluc":1,"smoke":0,"alco":0,"active":1,"age_years":50}'


AWS SageMaker Deployment
The model is deployed using a custom Docker container.
Steps:
1. Build and push Docker image to Amazon ECR
2. Create SageMaker model
3. Create endpoint configuration
4. Deploy endpoint
Deployment script:
python deploy_sagemaker.py



CI/CD Pipeline (GitHub Actions)

CI (Continuous Integration)
Triggered on push and pull requests:
- Linting (flake8)
- Unit tests (pytest)
- DVC pull
- Sanity pipeline execution

CD (Continuous Deployment)
Triggered on push to main:
- Reproduce DVC pipeline
- Run monitoring checks
- Push artifacts to S3
- Build Docker image (amd64)
- Push to ECR
- Deploy SageMaker endpoint


Monitoring
A basic monitoring script checks model performance:
python src/monitor.py
Current rule:
- Alert if accuracy < 0.70
This simulates drift detection in production pipelines.


Governance & Responsible AI Fairness
Model performance is evaluated across gender groups:
- Model performance is evaluated across gender subgroups by computing accuracy, precision, recall, and F1 score separately. This allows detection of potential disparities between groups, although no fairness mitigation techniques were applied in this project.
- Incident playbook: reports/incident_playbook.md
- Model audit log: reports/model_version_audit_log.md
Governance workflow
- Validate data
- Evaluate model performance
- Review fairness metrics
- Approve before deployment

Key Results
- Best model: Random Forest
- Accuracy: ~0.73
- Fairness gap: small but monitored


Lessons Learned:
- Data validation is critical (invalid blood pressure values were detected)
- Docker architecture must match deployment environment (amd64 vs arm)
- CI/CD pipelines require proper secret management
- Monitoring and governance are essential for production ML systems


Next Steps:
- Add advanced drift detection
- Implement model registry (MLflow)
- Improve fairness mitigation techniques
- Add canary deployment strategy



Reference

Ulianova, S. (2019). Cardiovascular disease dataset [Data set]. Kaggle. https://www.kaggle.com/datasets/sulianova/cardiovascular-disease-dataset
