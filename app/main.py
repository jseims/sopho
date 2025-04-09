from fastapi import FastAPI, Form, File, UploadFile, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from typing import List, Optional
from pydantic import BaseModel
import logging
import json
import db
import ast
import email_handler


# Database configuration
DEFAULT_PROMPT_SET = 0
MAX_PAGE_COUNT = 20
try:
  from localsettings import *
except:
  print("Error reading localsettings")

logger = logging.getLogger("api")
app = FastAPI()
templates = Jinja2Templates(directory='templates/')
app.mount('/template/static', StaticFiles(directory="static"), name="static")

# Html pages
@app.get("/")
async def index(request: Request):
    result = "Enter your name"
    return templates.TemplateResponse(
        "index.html", context={"request": request, "result": result}
    )

@app.get("/book")
async def book_view(request: Request, id):
    query = "SELECT * FROM book WHERE id = %s"
    prompt_response = list(db.query(query, [id]))
    book = prompt_response[0]
    return templates.TemplateResponse(
        "book.html", context={"request": request, "id": id, "book_title" : book['title']}
    )

@app.get("/text_search")
async def book_view(request: Request, id):
    query = "select b.title from book b, response_piece rp, prompt_response pr where rp.id = %s and rp.prompt_response_id = pr.id and b.id = pr.book_id;"
    prompt_response = list(db.query(query, [id]))
    book = prompt_response[0]
    return templates.TemplateResponse(
        "text_search.html", context={"request": request, "id": id, "book_title" : book['title']}
    )

@app.get("/test_me")
async def test_me(request: Request, book_id, response_piece_id):
    query = "SELECT * FROM book WHERE id = %s"
    prompt_response = list(db.query(query, [book_id]))
    book = prompt_response[0]
    return templates.TemplateResponse(
        "test_me.html", context={"request" : request, "book_id" : book_id, "response_piece_id" : response_piece_id, "book_title" : book['title']}
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


# API handlers
@app.get("/get_books")
async def get_books(request: Request):
    books = list(db.query("""SELECT * FROM book ORDER BY id DESC"""))
    return books

@app.get("/get_book_content")
async def get_book_content(book_id):
    result = {}


    query = "SELECT * FROM book WHERE id = %s"
    prompt_response = list(db.query(query, [book_id]))
    result['book_info'] = prompt_response[0]

    prompt_list = list(db.query("""SELECT id, name, label, position FROM prompt WHERE level = 1 AND prompt_set = %s ORDER BY position""", [DEFAULT_PROMPT_SET]))
    #result['prompt_list'] = prompt_list

    # not sure why this is here
    # result['subprompt_list'] = prompt_list

    prompt_response_list = []
    for prompt in prompt_list:
        item = {}
        item['prompt'] = prompt

        query = "SELECT * FROM prompt_response WHERE book_id = %s AND prompt_id = %s"
        prompt_response = list(db.query(query, [book_id, prompt['id']]))

        if len(prompt_response) != 1:
            # log this error
            continue

        prompt_response_id = prompt_response[0]['id']

        query = "SELECT * FROM response_piece WHERE prompt_response_id = %s ORDER BY position"
        response_pieces = list(db.query(query, [prompt_response_id]))
        str_bigint(response_pieces, ["id", "prompt_response_id"])
        item['response_list'] = response_pieces

        prompt_response_list.append(item)

    result['prompt_response_list'] = prompt_response_list

    return result

# for Javascript, we need to convert bigints into strings, sigh
def str_bigint(item_list, key_list):
    for item in item_list:
        for key in key_list:
            item[key] = str(item[key])

@app.get("/get_subresponse")
async def get_subresponse(response_piece_id):
    result = {}

    query = "SELECT * FROM prompt_response WHERE response_piece_id = %s ORDER BY prompt_id"
    prompt_responses = list(db.query(query, [response_piece_id]))

    prompt_response_list = []
    for prompt_response in prompt_responses:
        item = {}

        query = "SELECT id, name, label, position FROM prompt WHERE id = %s ORDER BY position"
        prompt = list(db.query(query, [prompt_response['prompt_id']]))[0]

        if prompt['name'] == 'test':
            continue

        item['prompt'] = prompt

        query = "SELECT * FROM response_piece WHERE prompt_response_id = %s ORDER BY position"
        response_pieces = list(db.query(query, [prompt_response['id']]))
        str_bigint(response_pieces, ["id", "prompt_response_id"])
        item['response_list'] = response_pieces
        prompt_response_list.append(item)

    result['subprompt_response_list'] = prompt_response_list

    return result


@app.get("/load_book_matches")
async def load_book_matches(id):

    query = "SELECT rp.matches, rp.text, rp.text_type, pr.book_id, b.title, b.image_url FROM response_piece rp, prompt_response pr, book b WHERE rp.id = %s AND rp.prompt_response_id = pr.id AND pr.book_id = b.id"
    rp_info = list(db.query(query, [id]))[0]
    response = {}

    if rp_info is not None:
        if rp_info['text_type'] == 'test_question':
            test_obj = ast.literal_eval(rp_info['text'])
            response['match_text'] = test_obj['explanation']
        else:
            response['match_text'] = rp_info['text']
        book_id = rp_info['book_id']
        matches = json.loads(rp_info['matches'])
        title = rp_info['title']
        image_url = rp_info['image_url']
        response['title'] = title
        response['image_url'] = image_url

        response['matches'] = matches
        if len(matches) > 0:
            match = matches[0]

            query = "SELECT * FROM book_content WHERE id = %s"
            content_info = list(db.query(query, [match]))[0]
            str_bigint([content_info], ["id"])
            response['content_info'] = content_info
            response['title'] = title
            response['image_url'] = image_url

            query = "SELECT max(page) FROM book_content WHERE book_id = %s"
            page_count_info = list(db.query(query, [book_id]))[0]
            response['max_page'] = page_count_info['max(page)']

            page = content_info['page']
            query = "SELECT id, text FROM book_content WHERE book_id = %s AND page = %s ORDER BY position"
            text_list = list(db.query(query, [book_id, page]))
            str_bigint(text_list, ["id"])
            response['text_list'] = text_list

    return response

@app.get("/load_match_index")
async def load_match_index(id):
    response = {}
    query = "SELECT * FROM book_content WHERE id = %s"
    content_info = list(db.query(query, [id]))[0]
    str_bigint([content_info], ["id"])
    response['content_info'] = content_info

    book_id = content_info['book_id']
    page = content_info['page']
    query = "SELECT id, text FROM book_content WHERE book_id = %s AND page = %s ORDER BY position"
    text_list = list(db.query(query, [book_id, page]))
    str_bigint(text_list, ["id"])
    response['text_list'] = text_list

    return response


@app.get("/load_page")
async def load_page(book_id, page, count):
    response = {}

    if int(count) > MAX_PAGE_COUNT:
        text_list = [{'id' : -1, 'text' : 'You have reached the maximum allowed page views for this book'}]
    else:
        query = "SELECT id, text FROM book_content WHERE book_id = %s AND page = %s ORDER BY position"
        text_list = list(db.query(query, [book_id, page]))
        str_bigint(text_list, ["id"])
    response['text_list'] = text_list

    return response

@app.get("/get_test_questions")
async def get_test_questions(book_id, response_piece_id):
    response = {}

    query = "SELECT * FROM book WHERE id = %s"
    prompt_response = list(db.query(query, [book_id]))
    response['book_info'] = prompt_response[0]
    questions = []

    #logger.warn(f"JOSH 1")

    if response_piece_id == '-1':
        # todo: make this work for other prompt_sets
        query = "SELECT id FROM prompt_response WHERE book_id = %s AND prompt_id = 25"
        prompt_list = list(db.query(query, [book_id]))
        for prompt in prompt_list:
            query = "SELECT text, id FROM response_piece WHERE prompt_response_id = %s"
            prompt_questions = list(db.query(query, [prompt['id']]))
            str_bigint(prompt_questions, ["id"])
            for question in prompt_questions:
                questions.append(question)
    else:
        query = "SELECT id, prompt_id FROM prompt_response WHERE response_piece_id = %s"
        prompt_list = list(db.query(query, [response_piece_id]))
        for prompt in prompt_list:
            query = "SELECT text, id, text_type FROM response_piece WHERE prompt_response_id = %s"
            response_pieces = list(db.query(query, [prompt['id']]))
            for response_piece in response_pieces:
                if response_piece['text_type'] == 'test_question':
                    questions.append(response_piece)

                # go another layer deeper
                query = "SELECT id, prompt_id FROM prompt_response WHERE response_piece_id = %s"
                deep_prompt_list = list(db.query(query, [response_piece['id']]))
                for deep_prompt in deep_prompt_list:
                    query = "SELECT text, id, text_type FROM response_piece WHERE prompt_response_id = %s"
                    deep_response_pieces = list(db.query(query, [deep_prompt['id']]))
                    for deep_response_piece in deep_response_pieces:
                        if deep_response_piece['text_type'] == 'test_question':
                            questions.append(deep_response_piece)
        str_bigint(questions, ["id"])

    response['question_list'] = questions

    return response


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

app.include_router(email_handler.router, prefix="/email")
