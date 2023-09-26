#!/usr/bin/env python

import requests
import sys
import time
import db
import openai
import hashlib
import random
from openai_multi_client import OpenAIMultiClient, Payload

OPENAI_API_KEY = ''

try:
  from localsettings import *
except:
  print("Error reading localsettings")

openai.api_key = OPENAI_API_KEY
model="gpt-4-0314"

# Remember to set the OPENAI_API_KEY environment variable to your API key
api = OpenAIMultiClient(endpoint="chats", data_template={"model": model}, max_retries=5)


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


def filter_prompts(prompts, level):
    level_prompts = []

    for prompt in prompts:
        prompt_level = int(prompt.get("level"))
        if prompt_level == level:
            level_prompts.append(prompt)

    return level_prompts


def response_exists(hash):
    # lookup by hash
    sql = "SELECT * FROM prompt_response WHERE prompt_hash = %s"
    args = [hash]
    rows = db.query(sql, args, False)
    return len(rows) != 0

def save_prompt_response(book_id, prompt_id, hash, system_text, prompt_text, response_text, llm, position, compute_time, prompt_tokens, response_tokens):
    # delete old one if exists
    sql = "DELETE FROM prompt_response WHERE book_id = %s AND prompt_id = %s AND position = %s"
    args = [book_id, prompt_id, position]
    db.query(sql, args)

    # save new
    id = random.randint(1, 18446744073709551615)
    args = {}
    args['id'] = id
    args['book_id'] = book_id
    args['prompt_id'] = prompt_id
    args['position'] = position
    args['created_on'] = int(time.time())
    args['prompt_hash'] = hash
    args['prompt_text'] = prompt_text
    args['response_text'] = response_text
    args['llm'] = llm
    args['compute_time'] = compute_time
    args['prompt_tokens'] = prompt_tokens
    args['response_tokens'] = response_tokens

    sql = insertFromDict("prompt_response", args)
    db.query(sql, args)

def on_result(result: Payload):
    print("on_result")
    if result.failed:
        print("Failed")
        print(result)
    else:
        start_time = result.metadata['start_time']
        book_id = result.metadata['book_id']
        prompt_id = result.metadata['prompt_id']
        hash = result.metadata['hash']
        system = result.metadata['system']
        prompt_text = result.metadata['prompt_text']
        model = result.metadata['model']
        position = result.metadata['position']
        response_text = result.response['choices'][0]['message']['content']
        prompt_tokens = result.response['usage']['prompt_tokens']
        completion_tokens = result.response['usage']['completion_tokens']

        compute_time = int(time.time() - start_time)
        print(result)
        save_prompt_response(book_id, prompt_id, hash, system, prompt_text, response_text, model, position, compute_time, prompt_tokens, completion_tokens)




def process_book(id, title, author, prompts, level, context):
    level_prompts = filter_prompts(prompts, level)

    for prompt in level_prompts:
        prompt_text = prompt.get("prompt_text")
        if context:
            prompt_text = prompt_text % (title, author, context)
        else:
            prompt_text = prompt_text % (title, author)

        #print(prompt_text)
        system = prompt.get("system_text")

        bstring = bytes("%s%s%s" % (prompt.get("id"), system, prompt_text), 'utf-8')
        hash_object = hashlib.sha256(bstring)
        hex_dig = hash_object.hexdigest()
        if not response_exists(hex_dig):

            api.request(data={
                "messages": [{"role": "system", "content": system},
                                {"role": "user", "content": prompt_text}]
            }, metadata={'start_time': time.time(), 'book_id' : id, 'prompt_id' : prompt.get("id"), 'hash' : hex_dig, 'system' : system, 'prompt_text' : prompt_text, 'model' : model}, callback=on_result)


            #chat_completion = openai.ChatCompletion.create(model=model, messages=[{"role": "system", "content": system},
            #                                                                {"role": "user", "content": prompt_text}])

        else:
            print("response already exists, skipping %s" % prompt_text)


def process_book_2(id, title, author, prompts, level, context):
    level_prompts = filter_prompts(prompts, level)

    for prompt in level_prompts:
        prompt_text = prompt.get("prompt_text")
        if context:
            prompt_text = prompt_text % (title, author, context)
        else:
            prompt_text = prompt_text % (title, author)

        #print(prompt_text)
        system = prompt.get("system_text")

        bstring = bytes("%s%s%s" % (prompt.get("id"), system, prompt_text), 'utf-8')
        hash_object = hashlib.sha256(bstring)
        hex_dig = hash_object.hexdigest()
        if not response_exists(hex_dig):

            api.request(data={
                "messages": [{"role": "system", "content": system},
                                {"role": "user", "content": prompt_text}]
            }, metadata={'start_time': time.time(), 'book_id' : id, 'prompt_id' : prompt.get("id"), 'hash' : hex_dig, 'system' : system, 'prompt_text' : prompt_text, 'model' : model, 'position' : 0}, callback=on_result)


            #chat_completion = openai.ChatCompletion.create(model=model, messages=[{"role": "system", "content": system},
            #                                                                {"role": "user", "content": prompt_text}])

        else:
            print("response already exists, skipping %s" % prompt_text)


def make_request(book_id, title, author, parent_item, name, prompt, position):
    request = None
    prompt_text = prompt.get("prompt_text")
    #print(prompt_text)
    if name == "test":
        answer_letter = parent_item['answer']
        answer = parent_item[answer_letter]
        prompt_text = prompt_text % (title, author, parent_item["question"], answer)
        #print(prompt_text)
    else:
        prompt_text = prompt_text % (title, author, parent_item)

    system = prompt.get("system_text")

    bstring = bytes("%s%s%s" % (prompt.get("id"), system, prompt_text), 'utf-8')
    hash_object = hashlib.sha256(bstring)
    hex_dig = hash_object.hexdigest()
    if not response_exists(hex_dig):

        request = {
        "messages": [{"role": "system", "content": system},
                        {"role": "user", "content": prompt_text}],
        "metadata" : {'start_time': time.time(), 'book_id' : book_id, 'prompt_id' : prompt.get("id"), 'hash' : hex_dig, 'system' : system, 'prompt_text' : prompt_text, 'model' : model, 'position' : position}}
        


    else:
        print("response already exists, skipping prompt id %s position %s\n" % (prompt.get("id"), position))
        nop = 1
    return request

def invoke_api(request_list, index, chunk_size):
    print("invoke_api with %s elements index %s chunk_size %s" % (len(request_list), index, chunk_size))
    start = index * chunk_size
    end = min(start + chunk_size, len(request_list))
    for i in range(start, end):
        request = request_list[i]
        #print(request["messages"])
        #print(request["metadata"])
        print("invoking api for request %s out of %s" % (i, len(request_list)))
        api.request(data={
            "messages": request["messages"]
        }, metadata=request["metadata"], callback=on_result)


def make_requests1():
    books = db.query("""SELECT * FROM book""")
    prompts = list(db.query("""SELECT * FROM prompt"""))

    for book in books:
        print(book.get('title'))
        process_book(book.get('id'), book.get('title'), book.get('author'), prompts, 1, None)

import json

def parse_response_text(text, name):
    #print("\n---TEXT---")
    #print(text)
    #print("---TEXT---")

    json_obj = json.loads(text)

    #print("\n---JSON---")
    #print("parsed into list with %s elements" % len(json_obj))
    #print("---JSON---")

    return json_obj

def make_requests2():
    prompts = list(db.query("""select r.id, r.book_id, r.prompt_id, p.name, b.title, b.author, r.response_text from prompt_response r, prompt p, book b where r.prompt_id = p.id and r.book_id = b.id and p.level = 1"""))
    request_list = []

    for prompt in prompts:
        #print(prompt)
        book_id = prompt['book_id']
        title = prompt['title']
        author = prompt['author']
        response_text = prompt['response_text']
        prompt_id = prompt['prompt_id']
        name = prompt['name']
        
        response_list = parse_response_text(response_text, name)
        #print(response_list)

        child_prompts = list(db.query("""SELECT * FROM prompt WHERE parent_id = %s""", [prompt_id]))

        position = 0
        for item in response_list:
            for child_prompt in child_prompts:
                request = make_request(book_id, title, author, item, name, child_prompt, position)
                if request != None:
                    request_list.append(request)
                position = position + 1

    return request_list

def dump_request(request, file):
    data = {"model" : model, "messages" : request["messages"], "metadata" : request["metadata"]}

    json_string = json.dumps(data)
    file.write(json_string + "\n")


def main(argv):
    request_list = []
    request_list = make_requests2()
    chunk_size = 10

    with open("requests.json", "w") as f:
        for request in request_list:
            print("doing it")
            dump_request(request, f)
            print("done")

if __name__ == "__main__":
   main(sys.argv[1:])

#{"model": "text-embedding-ada-002", "input": "0\n", "metadata": {"row_id": 1}}