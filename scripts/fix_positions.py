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


def fix_position(book_id, prompt_id):
    prompt_responses = list(db.query("""SELECT id, position FROM prompt_response WHERE book_id = %s AND prompt_id = %s ORDER BY position""", [book_id, prompt_id]))

    print(prompt_responses)
    for i in range(len(prompt_responses)):
        db.query("""UPDATE prompt_response SET position = %s WHERE id = %s""", [i, prompt_responses[i]['id']])



def main(argv):
    book_ids = list(db.query("""SELECT id FROM book"""))
    prompt_ids = list(db.query("""SELECT id FROM prompt"""))

    #print(book_ids)
    #print(prompt_ids)
    for book_id in book_ids:
        for prompt_id in prompt_ids:
            fix_position(book_id['id'], prompt_id['id'])

if __name__ == "__main__":
   main(sys.argv[1:])
