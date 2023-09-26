from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from starlette.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel,Field, validator

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
templates = Jinja2Templates(directory='templates/')
app.mount('/template/static', StaticFiles(directory="static"), name="static")

@app.get("/")
async def index(request: Request):
    result = "Enter your name"
    return templates.TemplateResponse(
        "index.html", context={"request": request, "result": result}
    )

@app.get("/get_books")
async def index(request: Request):
    cursor = conn.cursor()
    query = "SELECT * FROM book"
    cursor.execute(query)
    books = cursor.fetchall()

    return books