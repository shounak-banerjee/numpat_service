# #Setup
# import boto3
# import sagemaker
# region = boto3.Session().region_name
# client = boto3.client("sagemaker", region_name=region)

# #Role to give SageMaker permission to access AWS services.
# sagemaker_role = sagemaker.get_execution_role()

# #Get model from S3
# model_url = "s3://numpat-models/model.tar.gz"

# #Get container image (prebuilt example)
# from sagemaker import image_uris
# container = image_uris.retrieve("xgboost", region, "0.90-1")

# #Create model
# model_name = "collaboration_model"

# response = client.create_model(
#     ModelName = model_name,
#     ExecutionRoleArn = 'arn:aws:iam::541110341681:role/numpat_service',
#     Containers = [{
#         "Image": container,
#         "Mode": "SingleModel",
#         "ModelDataUrl": model_url,
#     }]
# )
# import boto3
# import sagemaker

# # Define your region
# region = boto3.Session().region_name

# # Create a SageMaker session
# sagemaker_session = sagemaker.Session(aws_access_key_id='AKIAX37FQSAY2HITDS46',
#                                      aws_secret_access_key='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',
#                                      region_name='ap-south-1',
#                                      role_arn='arn:aws:iam::541110341681:role/numpat_service')

# # Role to give SageMaker permission to access AWS services.
# sagemaker_role = sagemaker.get_execution_role()

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

# Specify your AWS access key and secret key (replace with your own credentials)
aws_access_key = "ASIAQVYUMFMUTA4V6L53"
aws_secret_key = "whafMKojUYlOr1WBenZH/64ucy0kQxO0N3BwcTeq"
AWS_SESSION_TOKEN="IQoJb3JpZ2luX2VjEGwaCmFwLXNvdXRoLTEiSDBGAiEA2IQ6PL/i/4dlKLO2Lmt5YsVHseCLcb4Uh00b4fECMsoCIQDlaeCGw6o3Z4LpGhHouEZDZTMh7M+cp/To7wyAF+FcmCqjAwiV//////////8BEAAaDDA0Njc1MDUwOTg2NSIMxVXWqFlyPmqvG2cxKvcC8nQwh6vLi5Lir7MzP3X5JiKw/FzZpZ3xeVNEVrVzZSksslcroydUAJskk9b0I3fj1OHBDcScnaBzh/AFRo0XnfR6DLeZ69iMnEvXmc0rCYCJRQd2shmqYxHFLwxyh8F1rIaA6XxwSZG4bSQeIQmDqUiYrOWiAJmLfbXWGYURJZDk8fa9JxvGpokXpZ7UiHR60B5xkAldKdi7//nJyhjjGf+yQWTHpbbQEXBIT6yiiK/hskzleIfKfu/+0+pwWmtYgrSteF3Ya4KxseI9Mn+dKGKrfJRP3T7zqLDLKUaWXuTTAftUsguS5yL2s19W2bMb5WOQ4pUdNEXoPwaXKPR3JoZr16WDausDGE+Fp6BPYRI0hU6sp7gj0N66MkrPMt8zdMPNc9tKgVKcP8eZCzMOecPvSQGiP1zigZiwsQafxbHAMkaDG5xaOHg01HMFrTgO05S1QvoxGGwpFFq4CdnkIZBMcO4cjPPKbJQlk+z9r33ewZOcoLT/MLik8KkGOqUBWwpRgT4R0OwyT3fkn/eDCrJyPaafePzNXxIWR4OZUN5tihcifaJBxHlX46ItrqQ093Y8cboUjcqgFYttPTETT9NanazZBD8i45FxWh6bmblC22TghMOrQCZn8nESdJh1+0RAUl2TC4UOAtf6rwgiEOXZQ5wZED+WbcP/3f6VcBnTGiUbdtpT0oAlpsBdHpf93Ek+apXYzkNsF4B7FgLxlsQPumYb"

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
