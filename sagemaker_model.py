# # Specify the ECR image URI for your custom container
ecr_image_uri = "046750509865.dkr.ecr.ap-south-1.amazonaws.com/numpat_service"

# # Create model
# model_name = "collaboration_model"

# # Define the container configuration
# container_config = {
#     "Image": ecr_image_uri,
#     "ModelDataUrl": model_url,  # Assuming you have the model data URL defined earlier
#     "Mode": "SingleModel",
# }

# # Create the SageMaker model
# response = sagemaker_session.create_model(
#     name=model_name,
#     role=sagemaker_role,
#     image_uri=ecr_image_uri,
#     container_def=container_config,
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

# Get model from S3
model_url = "s3://numpat-transformer-models/learning_and_development.tar.gz"

# # Get container image (prebuilt example)
# from sagemaker import image_uris
# container = image_uris.retrieve("xgboost", region, "0.90-1")

# Create model
model_name = "lnd-model"

response = sagemaker_client.create_model(
    ModelName=model_name,
    ExecutionRoleArn='arn:aws:iam::046750509865:role/EC2-ECR-Role',  # SageMaker role (you can change this if needed)
    Containers=[
        {
            "Image": ecr_image_uri,
            "Mode": "SingleModel",
            "ModelDataUrl": model_url,
        }
    ]
)
