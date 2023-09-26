#!/usr/bin/env python

import requests
import sys
import time
import db
import hashlib
import random
import argparse  # for running script from command line
import json

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

def save_prompt_response(book_id, prompt_id, hash, prompt_text, response_text, llm, position, compute_time, prompt_tokens, response_tokens):
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

def save_item(item):
    book_id = item[2]['book_id']
    prompt_id = item[2]['prompt_id']
    position = item[2]['position']
    hash = item[2]['hash'] 
    prompt_text = item[2]['prompt_text'] 
    model = item[2]['model'] 
    compute_time = 0
    prompt_tokens = item[1]['usage']['prompt_tokens']
    response_tokens = item[1]['usage']['completion_tokens']

    # damn, must hack this string :(
    str = item[1]['choices'][0]['message']['content']
    start = str.find('"', 15) + 1
    end = str.rfind('"')
    response_text = str[start:end]

    save_prompt_response(book_id, prompt_id, hash, prompt_text, response_text, model, position, compute_time, prompt_tokens, response_tokens)


def main(argv):
    # parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", default=None)
    args = parser.parse_args()
    filepath=args.file
    data = []

    with open(filepath) as f:
        for line in f:
            data.append(json.loads(line))

        print("%s rows " % len(data))
        for item in data:
            save_item(item)

if __name__ == "__main__":
   main(sys.argv[1:])

#{"model": "text-embedding-ada-002", "input": "0\n", "metadata": {"row_id": 1}}