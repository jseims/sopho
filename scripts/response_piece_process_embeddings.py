#!/usr/bin/env python

import requests
import sys
import time
import db
import hashlib
import random
import argparse  # for running script from command line
import json
import pinecone

try:
  from localsettings import *
except:
  print("Error reading localsettings")


def lookup_book_id(response_piece_id):
    sql = "SELECT pr.book_id FROM prompt_response pr, response_piece rp WHERE rp.id = %s AND rp.prompt_response_id = pr.id"
    args = [response_piece_id]
    result = list(db.query(sql, args))
    id = result[0]['book_id']
    return str(id)


def process_vector(item, index):
    id = str(item[2]['id'])

    # ugly fix for previous results.json having book embeddings 
    if not 'book_id' in item[2]:
        vector = item[1]['data'][0]['embedding']

        book_id = lookup_book_id(id)

        response = index.query(vector=vector, top_k=20, include_values=False, namespace=book_id)
        matches = response['matches']

        #print(matches)

        match_list = []
        for match in matches:
            book_content_id = match['id']
            match_list.append(book_content_id)

        match_str = json.dumps(match_list)

        # if we're here, assume it worked
        sql = "UPDATE response_piece SET matches = %s WHERE id = %s"
        args = [match_str, id]
        db.query(sql, args)


def main(argv):
    # parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", default="results.json")
    args = parser.parse_args()
    filepath=args.file
    data = []

    pinecone.init(api_key=PINECONE_API_KEY, environment=PINECONE_ENVIRONMENT)
    index = pinecone.Index("books")

    with open(filepath) as f:
        for line in f:
            data.append(json.loads(line))

        print("%s rows " % len(data))
        i = 0
        for item in data:
            process_vector(item, index)
            print("processed %s of %s" % (i, len(data)))
            i = i + 1

if __name__ == "__main__":
   main(sys.argv[1:])

#{"model": "text-embedding-ada-002", "input": "0\n", "metadata": {"row_id": 1}}
"""
import json
filepath = "test_results.json"
data = []

with open(filepath) as f:
    for line in f:
        data.append(json.loads(line))

item = data[0]
id = item[2]['id']
book_id = item[2]['book_id']
vector = item[1]['data'][0]['embedding']

import pinecone
PINECONE_API_KEY = "a3f482c3-3d28-4b3b-88d5-358c07c87805"
PINECONE_ENVIRONMENT = "us-east-1-aws"

pinecone.init(api_key=PINECONE_API_KEY, environment=PINECONE_ENVIRONMENT)


index = pinecone.Index("books")
pinecone.describe_index('books')


index.upsert(vectors = [(id, vector)], namespace = book_id)

index.query(vector=vector, top_k=20, include_values=False, namespace="2")


Test strings from Skin in the Game

1:
The notion of 'skin in the game' extends to the political and social spheres as well, as Taleb argues that politicians and policymakers should be directly affected by the consequences of their decisions. This ensures that they make choices that benefit society rather than pursuing their own self-interest or basing decisions on theoretical principles.

{'matches': [{'id': '6183113114425178474', 'score': 0.875473619, 'values': []},
             {'id': '5514030093728814362', 'score': 0.870997131, 'values': []},
             {'id': '15870503203733181541', 'score': 0.868371427, 'values': []},
             {'id': '16946029035099171968', 'score': 0.868251, 'values': []},
             {'id': '13028611064233342593', 'score': 0.867490411, 'values': []},
             {'id': '12183436270807989956', 'score': 0.863292813, 'values': []},
             {'id': '12701146638242059076', 'score': 0.862285197, 'values': []},
             {'id': '13749133391890407686', 'score': 0.858299494, 'values': []},
             {'id': '8484894111738944823', 'score': 0.853838682, 'values': []},
             {'id': '8726301562458397423', 'score': 0.853565872, 'values': []},
             {'id': '13318268919535949260', 'score': 0.853413701, 'values': []},
             {'id': '7552647116852926645', 'score': 0.851860285, 'values': []},
             {'id': '685332902810093508', 'score': 0.850518286, 'values': []},
             {'id': '4188677818375263979', 'score': 0.848710358, 'values': []},
             {'id': '8401717986959772520', 'score': 0.845018268, 'values': []},
             {'id': '14234847124154908112', 'score': 0.844851613, 'values': []},
             {'id': '6082783501632569774', 'score': 0.844833136, 'values': []},
             {'id': '4631084866445585905', 'score': 0.84300226, 'values': []},
             {'id': '4964727484540837166', 'score': 0.842976809, 'values': []},
             {'id': '4727021008323173751', 'score': 0.84171629, 'values': []}],


2:
Taleb discusses the historical development of probability theory and its application in modern risk management. He debunks the idea that theories established by well-known mathematicians like Blaise Pascal and Pierre-Simon Laplace are universally applicable, arguing that such theories are limited in their ability to predict real-world outcomes accurately. This demonstrates how over-reliance on theoretical models can lead to flawed decision-making in the real world.

{'matches': [{'id': '5308916538219259602', 'score': 0.85765624, 'values': []},
             {'id': '15907331054759851216', 'score': 0.852444649, 'values': []},
             {'id': '8555718029118859613', 'score': 0.852330387, 'values': []},
             {'id': '16451905502757369487', 'score': 0.846409142, 'values': []},
             {'id': '1273398438636674854', 'score': 0.840707302, 'values': []},
             {'id': '1678017456904605752', 'score': 0.839043617, 'values': []},
             {'id': '8318270550324825543', 'score': 0.836591423, 'values': []},
             {'id': '2712059583410533387', 'score': 0.834406614, 'values': []},
             {'id': '11336869953449186846', 'score': 0.833899379, 'values': []},
             {'id': '5840723334422704030', 'score': 0.83292675, 'values': []},
             {'id': '1323338676209215589', 'score': 0.832885, 'values': []},
             {'id': '11381734492024867153', 'score': 0.832060754, 'values': []},
             {'id': '376975749960446684', 'score': 0.831716299, 'values': []},
             {'id': '13243205643479872305', 'score': 0.831419945, 'values': []},
             {'id': '3622900194499374823', 'score': 0.831390262, 'values': []},
             {'id': '4131439904590833503', 'score': 0.831344187, 'values': []},
             {'id': '1525687501627298574', 'score': 0.831208527, 'values': []},
             {'id': '6072744328151277137', 'score': 0.829752088, 'values': []},
             {'id': '15080194109010214910', 'score': 0.829009295, 'values': []},
             {'id': '16296121811030855641',

3:
Using the example of ancient Roman engineers, Taleb demonstrates the importance of having skin in the game when it comes to making decisions about managing risk. According to an anecdote, Roman engineers were required to stand beneath the bridges they built while the structures were being tested as a way to ensure the safety of their designs. This practice demonstrates that when decision-makers have a personal stake in their choices, they're more likely to do a thorough, careful analysis of risk factors.


{'matches': [{'id': '16946029035099171968', 'score': 0.847929597, 'values': []},
             {'id': '7525449671593773186', 'score': 0.846577644, 'values': []},
             {'id': '13028611064233342593', 'score': 0.844995856, 'values': []},
             {'id': '6183113114425178474', 'score': 0.844052553, 'values': []},
             {'id': '8555718029118859613', 'score': 0.842347741, 'values': []},
             {'id': '15870503203733181541', 'score': 0.8420524, 'values': []},
             {'id': '11890013560016914123', 'score': 0.840693831, 'values': []},
             {'id': '5514030093728814362', 'score': 0.84051007, 'values': []},
             {'id': '18439994519426670201', 'score': 0.839544, 'values': []},
             {'id': '13318268919535949260', 'score': 0.839151859, 'values': []},
             {'id': '8726301562458397423', 'score': 0.838722229, 'values': []},
             {'id': '17308756923982974016', 'score': 0.838334143, 'values': []},
             {'id': '15877510967415860905', 'score': 0.834785581, 'values': []},
             {'id': '12701146638242059076', 'score': 0.8335796, 'values': []},
             {'id': '584910892854443146', 'score': 0.833253562, 'values': []},
             {'id': '4131439904590833503', 'score': 0.832538, 'values': []},
             {'id': '1678017456904605752', 'score': 0.832455397, 'values': []},
             {'id': '17538340974393181481', 'score': 0.832223356, 'values': []},
             {'id': '8484894111738944823', 'score': 0.83146894, 'values': []},
             {'id': '13749133391890407686',


4:
In discussing the societal impact of skin in the game, Taleb postulates that the ethics it promotes can function as a bulwark against the exploitation of others. When individuals are directly affected by the reverberations of their choices, especially when those choices involve others, they are less likely to champion decisions purely out of self-interest. The presence of skin in the game thus discourages leaders or influential figures from pursuing agendas that place undue burdens or consequences on those less powerful than themselves.

{'matches': [{'id': '16946029035099171968', 'score': 0.896873236, 'values': []},
             {'id': '6183113114425178474', 'score': 0.895795882, 'values': []},
             {'id': '13028611064233342593', 'score': 0.88760972, 'values': []},
             {'id': '12701146638242059076', 'score': 0.88278234, 'values': []},
             {'id': '4964727484540837166', 'score': 0.882494211, 'values': []},
             {'id': '5514030093728814362', 'score': 0.878914, 'values': []},
             {'id': '12183436270807989956', 'score': 0.877841175, 'values': []},
             {'id': '13749133391890407686', 'score': 0.87436, 'values': []},
             {'id': '13318268919535949260', 'score': 0.872484326, 'values': []},
             {'id': '15870503203733181541', 'score': 0.87145704, 'values': []},
             {'id': '8484894111738944823', 'score': 0.869771063, 'values': []},
             {'id': '4631084866445585905', 'score': 0.865402937, 'values': []},
             {'id': '15877510967415860905', 'score': 0.863667667, 'values': []},
             {'id': '13284961129288850188', 'score': 0.863627851, 'values': []},
             {'id': '7552647116852926645', 'score': 0.856861413, 'values': []},
             {'id': '6766148622919241568', 'score': 0.85672605, 'values': []},
             {'id': '6082783501632569774', 'score': 0.856612146, 'values': []},
             {'id': '7510016872750501866', 'score': 0.851996303, 'values': []},
             {'id': '17352678449485783794', 'score': 0.850985825, 'values': []},
             {'id': '17308756923982974016',



5:
In Chapter 8, Taleb speaks about the Golden Rule versus the Silver Rule. The Golden Rule states, 'Do unto others as you would have them do unto you,' while the Silver Rule states, 'Do not do unto others what you would not have them do unto you.' Taleb argues that the Silver Rule is more robust, as it encourages people to avoid harm to others, which has stronger skin-in-the-game elements.

{'matches': [{'id': '14203146974824646556', 'score': 0.91191411, 'values': []},
             {'id': '16063296365989593145', 'score': 0.90107739, 'values': []},
             {'id': '14427999440445842052', 'score': 0.878733456, 'values': []},
             {'id': '6627689440339971934', 'score': 0.869050622, 'values': []},
             {'id': '5163807331162995557', 'score': 0.863998055, 'values': []},
             {'id': '17270707696899731086', 'score': 0.857177734, 'values': []},
             {'id': '15986657092562550925', 'score': 0.848263383, 'values': []},
             {'id': '10741141199259514792', 'score': 0.843401968, 'values': []},
             {'id': '9647963068709298939', 'score': 0.837392032, 'values': []},
             {'id': '13602538769473049852', 'score': 0.83628118, 'values': []},
             {'id': '11308155778436721667', 'score': 0.830471694, 'values': []},
             {'id': '5884867103706246692', 'score': 0.828201652, 'values': []},
             {'id': '16946029035099171968', 'score': 0.826322913, 'values': []},
             {'id': '14234847124154908112', 'score': 0.825363219, 'values': []},
             {'id': '14891171554284663086', 'score': 0.825336814, 'values': []},
             {'id': '685332902810093508', 'score': 0.823360562, 'values': []},
             {'id': '15870503203733181541', 'score': 0.821356058, 'values': []},
             {'id': '5514030093728814362', 'score': 0.820345342, 'values': []},
             {'id': '1678017456904605752', 'score': 0.816991329, 'values': []},
             {'id': '8004070093690289710', 'score': 0.816563368, 'values': []}],


6:
Taleb believes the precautionary principle is useful when dealing with complex systems, as it can help mitigate potential negative consequences resulting from unforeseen events.

{'matches': [{'id': '1525687501627298574', 'score': 0.878401101, 'values': []},
             {'id': '4436838814586540395', 'score': 0.874592364, 'values': []},
             {'id': '6072744328151277137', 'score': 0.846133173, 'values': []},
             {'id': '16569334483368008576', 'score': 0.842538595, 'values': []},
             {'id': '3862439036235418278', 'score': 0.83526969, 'values': []},
             {'id': '11381734492024867153', 'score': 0.834241748, 'values': []},
             {'id': '15870503203733181541', 'score': 0.827752113, 'values': []},
             {'id': '9328550825515742620', 'score': 0.826280355, 'values': []},
             {'id': '2687652143642308406', 'score': 0.825347245, 'values': []},
             {'id': '2182293378902949783', 'score': 0.825205803, 'values': []},
             {'id': '17621073496011008009', 'score': 0.821461916, 'values': []},
             {'id': '9733299252108749913', 'score': 0.819885075, 'values': []},
             {'id': '11037984223018397841', 'score': 0.818697751, 'values': []},
             {'id': '16673070553692036826', 'score': 0.818197072, 'values': []},
             {'id': '16407425052887255015', 'score': 0.817940354, 'values': []},
             {'id': '9311411674637306657', 'score': 0.817769527, 'values': []},
             {'id': '5027352505889262952', 'score': 0.817641795, 'values': []},
             {'id': '14362861434095966811', 'score': 0.817188323, 'values': []},
             {'id': '9870405728546272506', 'score': 0.816498935, 'values': []},
             {'id': '3460684989574213418', 'score': 0.815232158, 'values': []}],

"""