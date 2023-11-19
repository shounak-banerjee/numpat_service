# # Create an endpoint configuration
# endpoint_config_name = 'collaboration-model'
# sagemaker.create_endpoint_config(
#     EndpointConfigName=endpoint_config_name,
#     ProductionVariants=[{
#         'InstanceType': 'ml.t2.medium',
#         'InitialInstanceCount': 1,
#         'ModelName': MODEL_NAME,
#         'VariantName': 'Variant-1'
#     }]
# )
import boto3
import sagemaker
import os
# Specify your AWS access key and secret key (replace with your own credentials)
aws_access_key=os.environ["AWS_ACCESS_KEY_ID"]
aws_secret_key=os.environ["AWS_SECRET_ACCESS_KEY"]
AWS_SESSION_TOKEN=os.environ["AWS_SESSION_TOKEN"]

# Specify your AWS region
region = "ap-south-1"

# Create a session with the specified credentials
session = boto3.Session(
    aws_access_key_id=aws_access_key,
    aws_secret_access_key=aws_secret_key,
    aws_session_token=AWS_SESSION_TOKEN,
    region_name=region
)

# Create a SageMaker client using the session
sagemaker_client = session.client("sagemaker")
model_name = "lnd-model"
# 1. Create an endpoint configuration
endpoint_config_name = "lnd-model-endpointconfig-5g"

# response = sagemaker_client.create_endpoint_config(
#     EndpointConfigName=endpoint_config_name,
#     # ProductionVariants=[
#     #     {
#     #         "VariantName": "DefaultVariant",
#     #         "ModelName": model_name,
#     #         "InstanceType": "ml.m5.large",  # Choose an appropriate instance type
#     #         "InitialInstanceCount": 1
#     #     }],
#     ProductionVariants=[
#         {
#             "ModelName": model_name,
#             "VariantName": "AllTraffic",
#             "ServerlessConfig": {
#                 "MemorySizeInMB": 3072,
#                 "MaxConcurrency": 10,
#                 "ProvisionedConcurrency": 10,
#             }
#         } 
#     ],
#     # DataCaptureConfig={
#     #     'EnableCapture': True,
#     #     'DestinationS3Uri': 's3://numpat_logs/',  # Replace with your S3 bucket and path
#     #     'CaptureOptions': [
#     #         {'CaptureMode': 'Output'},
#     #         {'CaptureMode': 'Input'}
#     #     ],
#     #     'InitialSamplingPercentage': 100
#     # }
# )

# 2. Create an endpoint using the endpoint configuration
# endpoint_name = "lnd-model-provisioned-endpoint"
endpoint_name = "lnd-model-5-g-endpoint"

response = sagemaker_client.create_endpoint(
    EndpointName=endpoint_name,
    EndpointConfigName=endpoint_config_name
)

print(f"Endpoint {endpoint_name} is being created. This might take a few minutes...")
