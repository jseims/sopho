#!/usr/bin/env python
from openai import OpenAI

try:
  from localsettings import *
except:
  print("Error reading localsettings")

def send_text_to_llm(llm_config, text):
    client = OpenAI(api_key=OPENAI_API_KEY)
    tools = []
    if llm_config.get('tools'):
        tools = [ { 'type': llm.get('tools') } ]

    response = client.responses.create(
        model = llm_config['model'],
        tools = tools,
        instructions = llm_config['prompt'],
        input = text
    )

    print(response.output_text)
    return response.output_text

