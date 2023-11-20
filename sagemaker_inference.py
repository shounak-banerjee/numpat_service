import boto3
import sagemaker
import json

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
sagemaker_client = session.client("runtime.sagemaker")

payload={
  "dimension": "L&sD",
  # "skills":["Collaboration"],
   "skills":["Problem solving and Critical Thinking","Communication","Collaboration","Creativity and Innovation"],
  "XTest":[["Due to climate change, extreme weather events such as hurricanes and droughts have become more frequent and intense. These events have severe implications for agriculture and food security. As a member of a global organization working on addressing climate change, you are tasked with developing a communication strategy to raise awareness about the impact of climate change on agriculture and promote sustainable farming practices.How would you develop a communication strategy to raise awareness about the impact of climate change on agriculture and promote sustainable farming practices?","My plan is grounded on reality. We'll portray the impacts of climate change on agriculture in vivid detail through arresting images and accessible anecdotes. Through entertaining courses and easily available online materials, we will demystify complicated scientific facts. We will demonstrate efficient sustainable agricultural techniques in partnership with stakeholders, empowering communities to embrace workable solutions and maintaining steady food security in the face of climate change."]]*20
}

payload_bytes = json.dumps(payload).encode('utf-8')
# endpoint_name = "collaboration-model-endpoint-serverless"
endpoint_name = "learning-and-development-provisioned"
response = sagemaker_client.invoke_endpoint(EndpointName=endpoint_name,
                                         ContentType='application/json',
                                         Body=payload_bytes)
 
result = json.loads(response["Body"].read().decode('utf-8'))
print(result)