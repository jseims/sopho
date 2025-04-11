#!/usr/bin/env python
import time
import boto3
from botocore.exceptions import ClientError
import db
from EmailDelegate import EmailDelegate
from MessageDelegate import MessageDelegate

try:
  from localsettings import *
except:
  print("Error reading localsettings")

# Create an SQS client
sqs = boto3.client('sqs', region_name=AWS_REGION)  # Update to your region

# Your queue URL (not just the name!)
queue_url = SQS_URL


while True:
    # Receive a message (long polling for up to 10 seconds)
    response = sqs.receive_message(
        QueueUrl=queue_url,
        MaxNumberOfMessages=1,
        WaitTimeSeconds=5  # enables long polling
    )

    messages = response.get('Messages', [])

    if messages:
        msg = messages[0]
        receipt_handle = msg['ReceiptHandle']
        body = msg['Body']

        # Optional: parse if JSON-encoded
        print("Received message:", body)

        # load the job with the id matching 'body'
        jobs = list(db.query("""SELECT * from job WHERE id = %s""", [body]))
        #print(jobs)
        if len(jobs) == 0:
           print("WARNING: no job found with id %s" % (body))
           continue

        # if it's an email job, use email delegate to get the message
        delegate = EmailDelegate(jobs[0]['msg_id'])

        # load the llm_config

        # call the llm

        # store the response

        # use email delegate to send the message
        delegate.send_message('hello world')

        #sqs.delete_message(
        #    QueueUrl=queue_url,
        #    ReceiptHandle=receipt_handle
        #)

    time.sleep(1)

