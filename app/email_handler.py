from fastapi import FastAPI, Form, File, UploadFile, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from typing import List, Optional
from pydantic import BaseModel
from fastapi import APIRouter
from email.parser import HeaderParser
import logging
import json
import db
import ast
import random
import boto3

router = APIRouter()
logger = logging.getLogger("api")

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


@router.post("_hook")
async def process_email_hook(request: Request):
    form = await request.form()

    logger.warn("==== Incoming email webhook ====")
    #for key, value in form.items():
    #    print(f"<key>{key}</key>: {value}")

    args = {}
    email_id = random.randint(1, 18446744073709551615)
    args['id'] = email_id
    args['email_from'] = form['from']
    args['email_to'] = form.get('to', None)
    args['email_cc'] = form.get('cc', None)
    args['email_text'] = form.get('text', None)
    args['subject'] = form.get('subject', None)
    args['spam_score'] = form.get('spam_score', 0.0)

    # parse header
    header_string = form.get('headers')
    parser = HeaderParser()
    headers = parser.parsestr(header_string)

    #print(f"Headers {header_string}")

    args['date'] = headers.get('Date', None)
    args['in_reply_to'] = headers.get('In-Reply-To', None)
    args['message_id'] = headers.get('Message-ID', None)
    args['email_references'] = headers.get('References', None)

    sql = insertFromDict("email", args)
    try:
        rows = db.query(sql, args)

        # now create the job
        args = {}
        job_id = random.randint(1, 18446744073709551615)
        args['id'] = job_id
        args['msg_id'] = email_id
        args['msg_type'] = 'email'
        args['status'] = 'waiting'
        sql = insertFromDict("job", args)
        rows = db.query(sql, args)

        # Create an SQS client
        sqs = boto3.client('sqs', region_name=AWS_REGION)  # Update to your region

        # Send the message to the queue
        response = sqs.send_message(
            QueueUrl=SQS_URL,
            MessageBody=str(job_id)
        )

    except Exception as e:      
        print("Error in process_email_hook saving to db")
        for key, value in form.items():
            print(f"<key>{key}</key>: {value}")
        print(e)

    return {"status": "received"}
