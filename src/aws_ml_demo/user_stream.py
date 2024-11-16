"""User data stream mock-up."""

import json
import os
import random
import time
import uuid

import boto3
import requests

AWS_REGION = os.getenv("AWS_REGION", "eu-central-1")
KINESIS_STREAM_NAME = os.getenv("KINESIS_STREAM_NAME")

client = boto3.client("kinesis", region_name=AWS_REGION)
partition_key = str(uuid.uuid4())

# Added 08/2020 since randomuser.me is starting to throttle API calls
# The following code loads 500 random users into memory
number_of_results = 500
response = requests.get(
    f"https://randomuser.me/api/?exc=login&results={number_of_results}"
)
data = response.json()["results"]

while True:
    # The following chooses a random user from the 500 random users pulled from the API in a single API call.
    random_user_index = int(random.uniform(0, (number_of_results - 1)))
    random_user = data[random_user_index]
    random_user = json.dumps(data[random_user_index])
    client.put_record(
        StreamName=KINESIS_STREAM_NAME,
        Data=random_user,
        PartitionKey=partition_key,
    )
    print(f"Sent user with id: {random_user_index}")
    time.sleep(random.uniform(0, 1))
