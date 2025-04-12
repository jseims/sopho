#!/usr/bin/env python
import time, random
import boto3
from botocore.exceptions import ClientError
from EmailDelegate import EmailDelegate
from MessageDelegate import MessageDelegate
import llm_utils
import db

try:
  from localsettings import *
except:
  print("Error reading localsettings")

def dictValuePad(key):
    return '%(' + str(key) + ')s'

def insertFromDict(table, dict):
    """Take dictionary object dict and produce sql for 
    inserting it into the named table"""
    sql = 'INSERT INTO ' + table
    sql += ' ('
    sql += ', '.join(dict)
    sql += ') VALUES ('
    sql += ', '.join(map(dictValuePad, dict))
    sql += ');'
    return sql


# Create an SQS client
sqs = boto3.client('sqs', region_name=AWS_REGION)  # Update to your region

# Your queue URL (not just the name!)
queue_url = SQS_URL

def save_llm_response(job_id, text, response):
    # save responses
    id = random.randint(1, 18446744073709551615)
    args = {}
    args['id'] = id
    args['job_id'] = job_id
    args['text'] = text
    args['response'] = response

    sql = insertFromDict("llm_response", args)
    try:
      db.query(sql, args)
    except Exception as e:      
        print("Error in save_llm_response")
        print(text)
        print(e)

    # save state on job table
    db.query("""UPDATE job SET status = %s WHERE id = %s""", ['done', job_id])


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
        llm_config = delegate.get_llm_config()

        if llm_config is None:
           # should save an error here
           continue

        text = delegate.get_conversation_text(llm_config['context_window'])

        # call the LLM
        if llm_config:
            response = llm_utils.send_text_to_llm(llm_config, text)

        if response:
            # store the response
            save_llm_response(jobs[0]['msg_id'], text, response)

            # use email delegate to send the message
            delegate.send_message(response)

        #sqs.delete_message(
        #    QueueUrl=queue_url,
        #    ReceiptHandle=receipt_handle
        #)

    time.sleep(1000)

