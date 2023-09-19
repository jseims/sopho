#!/usr/bin/env python

import requests
import sys
import time
import db
import openai
import hashlib
import random

OPENAI_API_KEY = ''

try:
  from localsettings import *
except:
  print("Error reading localsettings")

openai.api_key = OPENAI_API_KEY
model="gpt-4-0314"

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

def save_prompt_response(book_id, prompt_id, hash, system_text, prompt_text, response_text, llm, compute_time, prompt_tokens, response_tokens):
    # delete old one if exists
    sql = "DELETE FROM prompt_response WHERE book_id = %s AND prompt_id = %s"
    args = [book_id, prompt_id]
    db.query(sql, args)

    # save new
    id = random.randint(1, 18446744073709551615)
    args = {}
    args['id'] = id
    args['book_id'] = book_id
    args['prompt_id'] = prompt_id
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



def process_book(id, title, author, prompts, level, context):
    if level <= 3:
        level_prompts = filter_prompts(prompts, level)

        for prompt in level_prompts:
            prompt_text = prompt.get("prompt_text")
            if context:
                prompt_text = prompt_text % (title, author, context)
            else:
                prompt_text = prompt_text % (title, author)

            print(prompt_text)
            system = prompt.get("system_text")

            bstring = bytes("%s%s%s" % (prompt.get("id"), system, prompt_text), 'utf-8')
            hash_object = hashlib.sha256(bstring)
            hex_dig = hash_object.hexdigest()
            if not response_exists(hex_dig):
                start_time = time.time()

                chat_completion = openai.ChatCompletion.create(model=model, messages=[{"role": "system", "content": system},
                                                                                {"role": "user", "content": prompt_text}])

                compute_time = int(time.time() - start_time)
                print(chat_completion)
                save_prompt_response(id, prompt.get("id"), hex_dig, system, prompt_text, chat_completion.get("choices")[0].get("message").get("content"), model, compute_time, chat_completion.get("usage").get("prompt_tokens"), chat_completion.get("usage").get("completion_tokens"))
            else:
                print("response already exists, skipping %s" % prompt_text)


def main(argv):
    books = db.query("""SELECT * FROM book""")
    prompts = list(db.query("""SELECT * FROM prompt"""))

    for book in books:
        print(book.get('title'))
        process_book(book.get('id'), book.get('title'), book.get('author'), prompts, 1, None)

if __name__ == "__main__":
   main(sys.argv[1:])