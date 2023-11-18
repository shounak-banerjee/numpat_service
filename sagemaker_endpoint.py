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

# Specify your AWS access key and secret key (replace with your own credentials)
aws_access_key = "ASIAQVYUMFMUXEPYN7OR"
aws_secret_key = "QjrewSfdb5xb0aLhaZGMG/kEGlR7mKDIcEYM8tKz"
AWS_SESSION_TOKEN="IQoJb3JpZ2luX2VjEIP//////////wEaCmFwLXNvdXRoLTEiRzBFAiEAtAp+qju/f4lOJES/no9OLJJK8lpyZ42yT4F0ZCwL5EICIC5LdFm+YuTfb2zpXKIynQJC08QYO5q6M9iRB9gIke5/KqMDCK3//////////wEQABoMMDQ2NzUwNTA5ODY1Igz4jMR6OQB3QH8yGTcq9wIIRa//+6XmIfGXM+iHuJkyxM3/EmpHGE7QJWdTMWCBr/YD5NnNzCn9zxYL4NUVuCcZcIRDafDUKZFMAY5nPKwy8OjizcwV/tKsRhKOcvu76DIW3icSR1qB7h1xaEMRoJy79BYt5mTI0TIfLUhoUCESJFLIUjp/0IEApUiUeSsBPVncYwgjdUpb5VVPgKrBeFOHWpPh6tNloUxU6WQL5u2C2Rr8utu++CF8ICYX+gmG/e+hQ5V5UAyw4MoWUJPWwPJnda/CIdNac/nxLHd7TcG1kU0tzHtyU8VxuUfM0YREGpynL5+yajaoH8ajKPTQbHwTeFxL6sBJ8QgNp0KzqV0cih4dqMSNgU3BtzoSguvyW2cOWfUnMnVdMg0kqj4Nus6G1kUDT61Q1US5EFFbtylLP2XwNRGZlrw8WLj0kE5qsRM/kNscB7J4/x+6ystisYlcmJ2F5jMiJdWXue5S5K5NKBYXcy9RyPhrZLEZNE5yMQBBGyo/P+swi8H1qQY6pgHPm554UZT1nxgmCUfVBGBdkStC7KIDA0rjkBKTUZspKMd3yCrRbf7+p2LgWKMJ7dYj//creWANKW8xY4KJXARmnOlu/aroDeSKxsGc6+Qk6h7wnELoTbY5Gf/ZR5TJhR313vJV78euBJRUwo1e/ShLrDQ8GoSbMhU1KMFEZyLdTM/bwvQr+cnuCU0wes3lBk8hthjZtMJmF495c8nZ6B5tNLbk4fcL"

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
