from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from starlette.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel,Field, validator
import logging
import json

import MySQLdb

# Database configuration
try:
  from localsettings import *
except:
  print("Error reading localsettings")

db_config = {
    'host': 'localhost',
    'user': DATABASE_USER,
    'passwd': DATABASE_PASSWORD,
    'db': DATABASE_NAME,
}

# Create a connection to the database
conn = MySQLdb.connect(**db_config)


app = FastAPI()
logger = logging.getLogger("api")
templates = Jinja2Templates(directory='templates/')
app.mount('/template/static', StaticFiles(directory="static"), name="static")

@app.get("/")
async def index(request: Request):
    result = "Enter your name"
    return templates.TemplateResponse(
        "index.html", context={"request": request, "result": result}
    )

@app.get("/get_books")
async def get_books(request: Request):
    cursor = conn.cursor(MySQLdb.cursors.DictCursor)
    query = "SELECT * FROM book"
    cursor.execute(query)
    books = cursor.fetchall()

    return books

@app.get("/get_book_content")
async def get_book_content(book_id, prompt_id):
    result = {}

    cursor = conn.cursor(MySQLdb.cursors.DictCursor)

    query = "SELECT * FROM prompt WHERE level = 1"
    cursor.execute(query)
    prompt_list = cursor.fetchall()
    result['prompt_list'] = prompt_list

    query = "SELECT * FROM prompt WHERE parent_id = %s ORDER BY position"
    cursor.execute(query, [prompt_id])
    subprompt_list = cursor.fetchall()
    result['subprompt_list'] = subprompt_list

    query = "SELECT * FROM prompt_response WHERE book_id = %s AND prompt_id = %s"
    cursor.execute(query, [book_id, prompt_id])
    prompt_response = cursor.fetchone()
    response_list = json.loads(prompt_response['response_text'])
    result['response_list'] = response_list

    return result

@app.get("/get_subresponse")
async def get_book_content(book_id, prompt_id, position, parent_index : int):
    result = {}

    cursor = conn.cursor(MySQLdb.cursors.DictCursor)

    query = "SELECT * FROM prompt WHERE parent_id = %s ORDER BY position"
    cursor.execute(query, [prompt_id])
    prompt_list = cursor.fetchall()
    result['prompt_list'] = prompt_list

    if len(prompt_list) > parent_index:
        active_prompt_id = prompt_list[parent_index]['id']

        query = "SELECT * FROM prompt_response WHERE book_id = %s AND prompt_id = %s AND position = %s"
        cursor.execute(query, [book_id, active_prompt_id, position])
        prompt_response = cursor.fetchone()
        response_list = json.loads(prompt_response['response_text'])
        result['response_list'] = response_list
        result['active_prompt_id'] = active_prompt_id

    return result
