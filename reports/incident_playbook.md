# Incident Playbook

## Incident Type
Model performance degradation, failed deployment, or suspicious fairness drift.

## Detection
Incidents may be detected through:
- GitHub Actions pipeline failures
- SageMaker endpoint health check failures
- Accuracy dropping below 0.70 in `src/monitor.py`
- Fairness gap observed in subgroup metrics

## Severity Levels
- Sev 1: Endpoint unavailable or deployment failure
- Sev 2: Major drop in model accuracy or strong subgroup disparity
- Sev 3: Minor data quality issue with no immediate production impact

## Immediate Response
1. Check GitHub Actions logs
2. Check SageMaker endpoint status and CloudWatch logs
3. Verify the latest Docker image in ECR
4. Review evaluation and validation reports
5. Roll back to the last stable model if needed

## Root Cause Analysis
Investigate:
- recent code changes
- DVC pipeline outputs
- model metrics
- fairness metrics by gender
- SageMaker health check logs

## Recovery
- restore previous stable model artifact
- redeploy endpoint
- rerun CI/CD pipeline
- confirm endpoint responds to `/ping` and `/invocations`

## Prevention
- keep monitoring thresholds
- review fairness metrics before deployment
- use CI/CD gating
- maintain version audit logs