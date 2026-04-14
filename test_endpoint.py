import boto3
import json

runtime = boto3.client("sagemaker-runtime", region_name="us-east-1")

payload = {
    "gender": 1,
    "height": 170,
    "weight": 70,
    "ap_hi": 120,
    "ap_lo": 80,
    "cholesterol": 1,
    "gluc": 1,
    "smoke": 0,
    "alco": 0,
    "active": 1,
    "age_years": 50
}

response = runtime.invoke_endpoint(
    EndpointName="cardio-mlops-endpoint",
    ContentType="application/json",
    Body=json.dumps(payload)
)

result = response["Body"].read().decode("utf-8")
print(result)