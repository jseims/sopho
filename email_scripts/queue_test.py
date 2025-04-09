#!/usr/bin/env python

import boto3
from botocore.exceptions import ClientError


# If necessary, replace us-west-2 with the AWS Region you're using for Amazon SES.
AWS_REGION = "us-east-1"

# Create an SQS client
sqs = boto3.client('sqs', region_name=AWS_REGION)  # Update to your region

# Your queue URL (not just the name!)
queue_url = 'https://sqs.us-east-1.amazonaws.com/605520389418/sopho_jobs'

# Send the message
response = sqs.send_message(
    QueueUrl=queue_url,
    MessageBody="123"
)

print("Message sent! ID:", response['MessageId'])


# Receive a message (long polling for up to 10 seconds)
response = sqs.receive_message(
    QueueUrl=queue_url,
    MaxNumberOfMessages=1,
    WaitTimeSeconds=5  # enables long polling
)

messages = response.get('Messages', [])

if not messages:
    print("No messages in queue.")
else:
    msg = messages[0]
    receipt_handle = msg['ReceiptHandle']
    body = msg['Body']

    # Optional: parse if JSON-encoded
    print("Received message:", body)

    sqs.delete_message(
        QueueUrl=queue_url,
        ReceiptHandle=receipt_handle
    )
    print("Message deleted.")


# Receive a message (long polling for up to 10 seconds)
response = sqs.receive_message(
    QueueUrl=queue_url,
    MaxNumberOfMessages=1,
    WaitTimeSeconds=5  # enables long polling
)

messages = response.get('Messages', [])

if not messages:
    print("No messages in queue.")
else:
    msg = messages[0]
    receipt_handle = msg['ReceiptHandle']
    body = msg['Body']

    # Optional: parse if JSON-encoded
    print("Received message:", body)

    sqs.delete_message(
        QueueUrl=queue_url,
        ReceiptHandle=receipt_handle
    )
    print("Message deleted.")

