import time
import boto3

REGION = "us-east-1"
ACCOUNT_ID = "666109694562"

ROLE_ARN = "arn:aws:iam::666109694562:role/SageMakerExecutionRole-ALY4520"

MODEL_NAME = "cardio-mlops-model"
ENDPOINT_CONFIG_NAME = "cardio-mlops-endpoint-config"
ENDPOINT_NAME = "cardio-mlops-endpoint"

IMAGE_URI = f"{ACCOUNT_ID}.dkr.ecr.{REGION}.amazonaws.com/cardio-mlops:latest"
MODEL_DATA_URL = "s3://aly4520-mlops-luizza/model.tar.gz"

sm = boto3.client("sagemaker", region_name=REGION)


def delete_if_exists():
    try:
        sm.describe_endpoint(EndpointName=ENDPOINT_NAME)
        print(f"Deleting existing endpoint: {ENDPOINT_NAME}")
        sm.delete_endpoint(EndpointName=ENDPOINT_NAME)
        waiter = sm.get_waiter("endpoint_deleted")
        waiter.wait(EndpointName=ENDPOINT_NAME)
    except sm.exceptions.ClientError:
        pass

    try:
        sm.describe_endpoint_config(EndpointConfigName=ENDPOINT_CONFIG_NAME)
        print(f"Deleting existing endpoint config: {ENDPOINT_CONFIG_NAME}")
        sm.delete_endpoint_config(EndpointConfigName=ENDPOINT_CONFIG_NAME)
    except sm.exceptions.ClientError:
        pass

    try:
        sm.describe_model(ModelName=MODEL_NAME)
        print(f"Deleting existing model: {MODEL_NAME}")
        sm.delete_model(ModelName=MODEL_NAME)
    except sm.exceptions.ClientError:
        pass


def main():
    delete_if_exists()

    print("Creating SageMaker model...")
    sm.create_model(
        ModelName=MODEL_NAME,
        ExecutionRoleArn=ROLE_ARN,
        PrimaryContainer={
            "Image": IMAGE_URI,
            "ModelDataUrl": MODEL_DATA_URL,
        },
    )

    print("Creating endpoint config...")
    sm.create_endpoint_config(
        EndpointConfigName=ENDPOINT_CONFIG_NAME,
        ProductionVariants=[
            {
                "VariantName": "AllTraffic",
                "ModelName": MODEL_NAME,
                "InitialInstanceCount": 1,
                "InstanceType": "ml.m5.large",
                "InitialVariantWeight": 1.0,
            }
        ],
    )

    print("Creating endpoint...")
    sm.create_endpoint(
        EndpointName=ENDPOINT_NAME,
        EndpointConfigName=ENDPOINT_CONFIG_NAME,
    )

    print("Waiting for endpoint to be in service...")
    waiter = sm.get_waiter("endpoint_in_service")
    waiter.wait(EndpointName=ENDPOINT_NAME)

    print("Deployment complete.")
    print("Endpoint name:", ENDPOINT_NAME)


if __name__ == "__main__":
    main()