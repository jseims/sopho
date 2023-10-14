from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
#from pydantic import BaseModel,Field, validator
import logging
import json
import db


# Database configuration
try:
  from localsettings import *
except:
  print("Error reading localsettings")

app = FastAPI()
logger = logging.getLogger("api")
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
    return templates.TemplateResponse(
        "book.html", context={"request": request, "id": id}
    )

@app.get("/text_search")
async def book_view(request: Request, id):
    return templates.TemplateResponse(
        "text_search.html", context={"request": request, "id": id}
    )

@app.get("/test_me")
async def test_me(request: Request, book_id):
    return templates.TemplateResponse(
        "test_me.html", context={"request": request, "book_id": book_id}
    )


# API handlers
@app.get("/get_books")
async def get_books(request: Request):
    books = list(db.query("""SELECT * FROM book"""))

    return books

@app.get("/get_book_content")
async def get_book_content(book_id, prompt_id):
    result = {}


    query = "SELECT * FROM book WHERE id = %s"
    prompt_response = list(db.query(query, [book_id]))
    result['book_info'] = prompt_response[0]

    prompt_list = list(db.query("""SELECT * FROM prompt WHERE level = 1"""))
    result['prompt_list'] = prompt_list

    subprompt_list = list(db.query("""SELECT * FROM prompt WHERE level = 1"""))
    result['subprompt_list'] = subprompt_list

    query = "SELECT * FROM prompt_response WHERE book_id = %s AND prompt_id = %s"
    prompt_response = list(db.query(query, [book_id, prompt_id]))[0]

    query = "SELECT * FROM response_piece WHERE prompt_response_id = %s ORDER BY position"
    response_pieces = list(db.query(query, [prompt_response['id']]))
    result['response_list'] = response_pieces

    return result

# for Javascript, we need to convert bigints into strings, sigh
def str_bigint(item_list, key_list):
    for item in item_list:
        for key in key_list:
            item[key] = str(item[key])

@app.get("/get_subresponse")
async def get_subresponse(book_id, prompt_id, position, parent_index : int):
    result = {}


    query = "SELECT * FROM prompt WHERE parent_id = %s ORDER BY position"
    prompt_list = list(db.query(query, [prompt_id]))
    result['prompt_list'] = prompt_list

    if len(prompt_list) > parent_index:
        active_prompt_id = prompt_list[parent_index]['id']

        query = "SELECT * FROM prompt_response WHERE book_id = %s AND prompt_id = %s AND position = %s"
        prompt_response = list(db.query(query, [book_id, active_prompt_id, position]))[0]

        query = "SELECT * FROM response_piece WHERE prompt_response_id = %s ORDER BY position"
        response_pieces = list(db.query(query, [prompt_response['id']]))
        str_bigint(response_pieces, ["id", "prompt_response_id"])

        result['response_list'] = response_pieces
        result['active_prompt_id'] = active_prompt_id

    return result

@app.get("/load_book_matches")
async def load_book_matches(id):

    query = "SELECT rp.matches, rp.text, pr.book_id, b.title, b.image_url FROM response_piece rp, prompt_response pr, book b WHERE rp.id = %s AND rp.prompt_response_id = pr.id AND pr.book_id = b.id"
    rp_info = list(db.query(query, [id]))[0]
    response = {}

    if rp_info is not None:
        response['match_text'] = rp_info['text']
        book_id = rp_info['book_id']
        matches = json.loads(rp_info['matches'])
        title = rp_info['title']
        image_url = rp_info['image_url']

        response['matches'] = matches
        if len(matches) > 0:
            match = matches[0]

            query = "SELECT * FROM book_content WHERE id = %s"
            content_info = list(db.query(query, [match]))[0]
            content_info['title'] = title
            content_info['image_url'] = image_url
            str_bigint([content_info], ["id"])
            response['content_info'] = content_info

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
async def load_page(book_id, page):
    response = {}
    query = "SELECT id, text FROM book_content WHERE book_id = %s AND page = %s ORDER BY position"
    text_list = list(db.query(query, [book_id, page]))
    str_bigint(text_list, ["id"])
    response['text_list'] = text_list
    cursor.close()

    return response