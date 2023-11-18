import boto3
import sagemaker
import json

# Specify your AWS access key and secret key (replace with your own credentials)
aws_access_key = "ASIAQVYUMFMU2YMFCCGK"
aws_secret_key = "+9nRR49J140Oh0sJZvQDuUdeBZXivaeeJesBA7Z2"
AWS_SESSION_TOKEN="IQoJb3JpZ2luX2VjELX//////////wEaCmFwLXNvdXRoLTEiSDBGAiEAt25l7jIoH2hOvlfCsHGmOjQD2Yn7rEdls5qhtMn15OgCIQDxpsHtp43vwTNAwuU1qWpIppw0neCJiILHRVYMrOcnjSqjAwje//////////8BEAAaDDA0Njc1MDUwOTg2NSIMfe4FPSYE651IdSHYKvcCQ/q/NN3JfbcoUeSGhYXfAWT0OWh0yFJOfX5dZ3m1FAMvmgZIQ4H1EFZc/37KeXCvRuCUH2d9eZQ/CK5Ou6rYw/IZgRFzc9okdgmxvhP7HwXDjhxi7QwNbD3MUnkBTpAiLcmH08qCve0uqYmISbRqELWtk/kmzZDYxZxrlYo6BjlF/o5oUjBkHrhMvObyyEtCK3n9u8VEbgjfCIQQqODMtV/ksnapp9PXO4vpu2uDSz++f3MD6y2LMPG3dP+IxqY3fKYdVbVtMNJ6rVvhzLjXvUbP1FVTvd069aX69SedMOIYM1VukDEv7mMqXx4Kxrwj6ugydB/YSHS7rWozt35L9+MdQ0BJau9UxwUocURfMqZXSAczbZvItQ/YXxT8J7cHiXdNt2dl3vmnHFho5rMugLOCn9NojThtq0Qi9TO9BmX39k9t7XdVkX/yME8H8D4CrvaEEqqvlRac2Vd0rYfYViUkiYAHySSrv3i/zjWb0Chxbmrw2kW5MMimgKoGOqUBXx1dsOHmNXQF5BIPNkda3ARrk46zEhF2dgYrN0RTZexsmn1Q8fkdLDWRTuYGTtS7evSjGd3MKk6armoUA6E/BD+j0vHBnNf35Yw2QBufdptW5Wl7i5UXuh9RlM4K84whLzsF/QFK1ZKPFiR2rNNLEhNA2guo8fQ7IbTbXdxsWvFjvlNdoDdcV5MANECvNmoy/V5TxlP1LfIIE9pTYm2dY7GaXZtC"

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
  "XTest":[["Due to climate change, extreme weather events such as hurricanes and droughts have become more frequent and intense. These events have severe implications for agriculture and food security. As a member of a global organization working on addressing climate change, you are tasked with developing a communication strategy to raise awareness about the impact of climate change on agriculture and promote sustainable farming practices.How would you develop a communication strategy to raise awareness about the impact of climate change on agriculture and promote sustainable farming practices?","My plan is grounded on reality. We'll portray the impacts of climate change on agriculture in vivid detail through arresting images and accessible anecdotes. Through entertaining courses and easily available online materials, we will demystify complicated scientific facts. We will demonstrate efficient sustainable agricultural techniques in partnership with stakeholders, empowering communities to embrace workable solutions and maintaining steady food security in the face of climate change."],["Due to climate change, extreme weather events such as hurricanes and droughts have become more frequent and intense. These events have severe implications for agriculture and food security. As a member of a global organization working on addressing climate change, you are tasked with developing a communication strategy to raise awareness about the impact of climate change on agriculture and promote sustainable farming practices.How would you develop a communication strategy to raise awareness about the impact of climate change on agriculture and promote sustainable farming practices?","My plan is grounded on reality. We'll portray the impacts of climate change on agriculture in vivid detail through arresting images and accessible anecdotes. Through entertaining courses and easily available online materials, we will demystify complicated scientific facts. We will demonstrate efficient sustainable agricultural techniques in partnership with stakeholders, empowering communities to embrace workable solutions and maintaining steady food security in the face of climate change."]]
}

payload_bytes = json.dumps(payload).encode('utf-8')
# endpoint_name = "collaboration-model-endpoint-serverless"
endpoint_name = "lnd-model-provisioned-endpoint"
response = sagemaker_client.invoke_endpoint(EndpointName=endpoint_name,
                                         ContentType='application/json',
                                         Body=payload_bytes)
 
result = json.loads(response["Body"].read().decode('utf-8'))
print(result)