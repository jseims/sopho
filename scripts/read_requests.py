#!/usr/bin/env python

import sys
import time
import db
import random
import argparse  # for running script from command line
import json
import ast

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



def save_prompt_response(book_id, prompt_id, hash, prompt_text, response_list, llm, response_piece_id, compute_time, prompt_tokens, response_tokens, text_type):
    # delete old prompt_response if exists
    sql = "SELECT id FROM prompt_response WHERE book_id = %s AND prompt_id = %s AND response_piece_id = %s"
    args = [book_id, prompt_id, response_piece_id]
    ids = list(db.query(sql, args))
    for id_obj in ids:
        id = id_obj['id']
        sql = "DELETE FROM prompt_response WHERE id = %s"
        args = [id]
        db.query(sql, args)

        sql = "DELETE FROM response_piece WHERE prompt_response_id = %s"
        args = [id]
        db.query(sql, args)

    # find type of prompt
    sql = "SELECT name FROM prompt WHERE id = %s"
    args = [prompt_id]
    names = list(db.query(sql, args))
    name = names[0]['name']
    text_type = "book_text"
    if name == "test":
        text_type = "test_question"

    # save new
    id = random.randint(1, 18446744073709551615)
    args = {}
    args['id'] = id
    args['book_id'] = book_id
    args['prompt_id'] = prompt_id
    if response_piece_id > 0:
        args['response_piece_id'] = response_piece_id
    args['created_on'] = int(time.time())
    args['prompt_hash'] = hash
    args['prompt_text'] = prompt_text
    args['llm'] = llm
    args['compute_time'] = compute_time
    args['prompt_tokens'] = prompt_tokens
    args['response_tokens'] = response_tokens

    sql = insertFromDict("prompt_response", args)
    db.query(sql, args)

    position = 0
    for text in response_list:
        rp_id = random.randint(1, 18446744073709551615)
        args = {}
        args['id'] = rp_id
        args['prompt_response_id'] = id
        args['position'] = position
        args['text'] = text
        args['text_type'] = text_type
        sql = insertFromDict("response_piece", args)
        db.query(sql, args)
        position = position + 1

def parse_response_text(text, name):
    response_list = []
    if name == "test":
        try:
            response_list = json.loads(text)
        except ValueError:  # includes simplejson.decoder.JSONDecodeError
            response_list = ast.literal_eval(text)
    else:
        response_list = text.split("\n\n")
        # remove responses that are too short
        response_list = list(filter(lambda x: len(x) > 50, response_list))

    return response_list

def save_item(item):
    book_id = item[2]['book_id']
    prompt_id = item[2]['prompt_id']
    response_piece_id = item[2]['response_piece_id']
    hash = item[2]['hash'] 
    prompt_text = item[2]['prompt_text'] 
    model = item[2]['model'] 
    compute_time = 0
    prompt_tokens = item[1]['usage']['prompt_tokens']
    response_tokens = item[1]['usage']['completion_tokens']

    # damn, must hack this string :(
    str = item[1]['choices'][0]['message']['content']
    #start = str.find('"', 15) + 1
    #end = str.rfind('"')
    #response_text = str[start:end]


    # find type of prompt
    sql = "SELECT name FROM prompt WHERE id = %s"
    args = [prompt_id]
    names = list(db.query(sql, args))
    name = names[0]['name']
    text_type = "book_text"
    if name == "test":
        text_type = "test_question"
    if name == "discussion":
        text_type = 'plain_text'

    response_list = parse_response_text(str, name)

    for item in response_list:
        #print("'%s'" % item)
        nop = 1

    # assume error if too short
    if len(response_list) > 1:
        save_prompt_response(book_id, prompt_id, hash, prompt_text, response_list, model, response_piece_id, compute_time, prompt_tokens, response_tokens, text_type)
        nop = 1
    else:
        print("Error in parsing %s" % str)


def main(argv):
    # parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", default="results.json")
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
"""
import json
text = "[\n{'question': 'What is a prominent theme among the factions in The Three-Body Problem?',\n'A)': 'Trisolaran superiority',\n'B)': 'Human superiority',\n'C)': 'Disagreement',\n'D)': 'Alien technology',\n'answer': 'C)',\n'explanation': 'The summary highlights disagreement as a prominent theme among the factions. They all differ on the best reaction to the arrival of the Trisolarans.'},\n\n{'question': 'What is the stance of some factions on the Trisolarans?',\n'A)': 'They should be met with peace and camaraderie',\n'B)': 'They should be ignored',\n'C)': 'They should be fought with advanced technology',\n'D)': 'They should be treated like ordinary humans',\n'answer': 'A)',\n'explanation': 'Part of the factions believes that it could be possible to coexist with the Trisolarans and suggests meeting with peace and camaraderie.'},\n\n{'question': 'How do other factions perceive the Trisolarans?',\n'A)': 'As potential allies',\n'B)': 'As a threat',\n'C)': 'As technologically backward creatures',\n'D)': 'As inferior beings',\n'answer': 'B)',\n'explanation': 'Conversely, other factions perceive the Trisolarans as a threat and argue for hostility against them.'},\n\n{'question': 'What does this debate reflect about humanity?',\n'A)': 'Humanity\\'s advanced technology',\n'B)': 'Humanity\\'s fear of the unknown',\n'C)': 'Humanity\\'s complex nature',\n'D)': 'Humanity\\'s superiority',\n'answer': 'C)',\n'explanation': 'The summary underscores that the debate reflects humanity\\'s complex nature, showing various reactions to an alien encounter.'},\n\n{'question': 'What reactions range from humanity to an alien encounter?',\n'A)': 'Indifference and aloofness',\n'B)': 'Hate and disgust',\n'C)': 'Fear and defiance to acceptance and cooperation',\n'D)': 'Curiosity and excitement',\n'answer': 'C)',\n'explanation': 'The reactions of humanity to the alien encounter range from fear and defiance to acceptance and cooperation.'},\n\n{'question': 'Which viewpoint is not mentioned in the given discussion?',\n'A)': 'Ignoring the Trisolarans',\n'B)': 'Being hostile towards the Trisolarans',\n'C)': 'Accepting the Trisolarans',\n'D)': 'Befriending the Trisolarans',\n'answer': 'A)',\n'explanation': 'The summary does not mention any factions advocating to ignore the Trisolarans.'},\n\n{'question': 'What is the condition necessary for factions wanting peace and camaraderie?',\n'A)': 'The Trisolarans reciprocating the same feelings',\n'B)': 'The Trisolarans being technologically inferior',\n'C)': 'The Trisolarans invading earth',\n'D)': 'Co-existence with the Trisolarans',\n'answer': 'D)',\n'explanation': 'The factions advocating for peace and camaraderie believe in the possibility of co-existing with the Trisolarans.'},\n\n{'question': 'What does the disagreement among the factions indicate about their perceptions of the Trisolarans?',\n'A)': 'Unpredictability',\n'B)': 'Different socio-political ideologies',\n'C)': 'Fear of being overpowered',\n'D)': 'Varied scientific theories',\n'answer': 'B)',\n'explanation': 'The disagreement among factions concerning the Trisolarans indicates differing socio-political ideologies among the groups.'},\n\n{'question': 'Who does the hostility intend to be directed against?',\n'A)': 'The factions advocating for acceptance',\n'B)': 'The factions neglecting the issue',\n'C)': 'The Trisolarans',\n'D)': 'The factions advocating for hostility',\n'answer': 'C)',\n'explanation': 'The hostility is suggested to be directed against the Trisolarans according to some factions.'},\n\n{'question': 'What response is not mentioned regarding humanity\\'s complexity?',\n'A)': 'Fear',\n'B)': 'Indifference',\n'C)': 'Defiance',\n'D)': 'Acceptance',\n'answer': 'B)',\n'explanation': 'The summary does not mention indifference as a part of humanity's complex responses to an alien encounter.'}\n]"
response_list = json.loads(text)


import db
from localsettings import *
book_id = 3
position = 3
prompt_id = 21

query = "SELECT * FROM prompt WHERE parent_id = %s AND prompt_set = %s AND name != 'test' ORDER BY position"
prompt_list = list(db.query(query, [prompt_id, DEFAULT_PROMPT_SET]))

prompt = prompt_list[0]
item = {}
item['prompt'] = prompt

query = "SELECT * FROM prompt_response WHERE book_id = %s AND prompt_id = %s AND position = %s"
prompt_response = list(db.query(query, [book_id, prompt['id'], position]))

if len(prompt_response) != 1:
    # log this error
    continue

prompt_response_id = prompt_response[0]['id']

query = "SELECT * FROM response_piece WHERE prompt_response_id = %s ORDER BY position"
response_pieces = list(db.query(query, [prompt_response_id]))
item['response_list'] = response_pieces

"""