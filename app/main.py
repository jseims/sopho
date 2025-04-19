from fastapi import FastAPI, Form, File, UploadFile, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import logging
import json
import db
import ast
import email_handler
import book_handler

app = FastAPI()
app.mount('/template/static', StaticFiles(directory="static"), name="static")

# Database configuration
DEFAULT_PROMPT_SET = 0
MAX_PAGE_COUNT = 20
try:
  from localsettings import *
except:
  print("Error reading localsettings")

logger = logging.getLogger("api")
templates = Jinja2Templates(directory='templates/')

@app.get("/")
async def index(request: Request):
    result = "Enter your name"
    return templates.TemplateResponse(
        "index.html", context={"request": request, "result": result}
    )

@app.get("/about")
async def about(request: Request):
    return templates.TemplateResponse(
        "about.html", context={"request" : request}
    )

@app.get("/contact")
async def about(request: Request):
    return templates.TemplateResponse(
        "contact.html", context={"request" : request}
    )


import boto3
from botocore.exceptions import ClientError

class Message(BaseModel):
    email: str
    msg: str 


@app.post("/contact_us")
async def contact_us(msg: Message):
    logger.warn(msg)

    # Replace sender@example.com with your "From" address.
    # This address must be verified with Amazon SES.
    SENDER = "josh@hitplay.com"

    # Replace recipient@example.com with a "To" address. If your account 
    # is still in the sandbox, this address must be verified.
    RECIPIENT = "josh@hitplay.com"

    # Specify a configuration set. If you do not want to use a configuration
    # set, comment the following variable, and the 
    # ConfigurationSetName=CONFIGURATION_SET argument below.
    #CONFIGURATION_SET = "ConfigSet"

    # If necessary, replace us-west-2 with the AWS Region you're using for Amazon SES.
    AWS_REGION = "us-east-1"

    # The subject line for the email.
    SUBJECT = "Contact Us Message from Sopho"

    # The email body for recipients with non-HTML email clients.
    BODY_TEXT = ("Email : %s\n\nText: %s" % (msg.email, msg.msg))
                
    # The character encoding for the email.
    CHARSET = "UTF-8"

    # Create a new SES resource and specify a region.
    client = boto3.client('ses',region_name=AWS_REGION)

    # Try to send the email.
    try:
        #Provide the contents of the email.
        response = client.send_email(
            Destination={
                'ToAddresses': [
                    RECIPIENT,
                ],
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': CHARSET,
                        'Data': BODY_TEXT,
                    },
                    'Text': {
                        'Charset': CHARSET,
                        'Data': BODY_TEXT,
                    },
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': SUBJECT,
                },
            },
            Source=SENDER,
            # If you are not using a configuration set, comment or delete the
            # following line
            #ConfigurationSetName=CONFIGURATION_SET,
        )
    # Display an error if something goes wrong.	
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("Email sent! Message ID:"),
        print(response['MessageId'])    



# include all the book handling logic in a separate file
app.include_router(book_handler.router, prefix="/book")

# include all the email handling logic in a separate file
app.include_router(email_handler.router, prefix="/email")
