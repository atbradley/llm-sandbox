import os

import yaml
import time

import openai
from dotenv import load_dotenv

load_dotenv()

OUTPUT_FOLDER = os.getenv("OUTPUT_FOLDER")
MODEL = os.getenv("MODEL", "gpt-4o-latest")


openai.api_key = os.getenv("API_KEY")
URL_BASE = os.getenv("URL_BASE")

client = openai.OpenAI(
    api_key=os.getenv("API_KEY"),
    base_url=URL_BASE,
)

sys_msg = input("Enter the system message: ")
messages = [
    {"role": "system", "content": sys_msg},
]

filename = f"convo{time.time_ns()}.yaml"

while True:
    print()
    prompt = input("Enter your text or 'q' to quit: ")

    if prompt == "q":
        break

    messages.append({"role": "user", "content": prompt})
    print("Sending...")

    response = client.chat.completions.create(
        model=MODEL, messages=messages, n=1  # We can ask for more possible responses.
    )

    print("Response:", response.choices[0].message.content)
    messages.append(
        {
            "role": response.choices[0].message.role,
            "content": response.choices[0].message.content,
        }
    )
    print("Tokens: ", response.usage.total_tokens)

    yaml.dump(
        messages,
        open(os.path.join(OUTPUT_FOLDER, filename), "w"),
        indent=4,
        Dumper=yaml.SafeDumper,
    )

# print(messages)
