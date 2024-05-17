import os
import json

import yaml
import time

import openai
from dotenv import load_dotenv

load_dotenv()

MODEL = os.getenv("MODEL", "gpt-4") 
openai.api_key = os.getenv("API_KEY")

sys_msg = """
    Perform sentiment analysis on each user message and return the only the 
    word "positive", "negative", "neutral", or "unknown". 
"""

while True:
    messages = [
            {"role": "system", "content": sys_msg.strip()},
    ]
    filename = f"sentiment{time.time_ns()}.yaml"
    print()
    prompt = input("Enter your text or 'q' to quit: ")    
    
    if prompt == "q":
        break

    messages.append({"role": "user", "content": prompt})
    print("Sending...")

    response=openai.ChatCompletion.create(
        model=MODEL,
        messages=messages,
        n=1  # We can ask for more possible responses.
    )

    print("Response:", response['choices'][0]['message']['content'])
    messages.append(response['choices'][0]['message'])
    print("Tokens: ", response['usage']['total_tokens'])

    jsondata = json.dumps(messages, indent=4)
    yamldata = json.loads(jsondata)
    yaml.dump(yamldata, open(filename, "w"), indent=4, Dumper=yaml.SafeDumper)

#print(messages)
