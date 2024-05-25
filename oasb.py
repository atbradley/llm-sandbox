import glob
import json
import os
import time

from dotenv import load_dotenv
import openai
import yaml

load_dotenv()

OUTPUT_FOLDER = os.getenv("OUTPUT_FOLDER")
PROMPT_FOLDER = os.getenv("PROMPT_FOLDER")
MODEL = os.getenv("MODEL", "gpt-4")
openai.api_key = os.getenv("API_KEY")

# TODO: New version that uses Chat Completion API. and sends a list of messages
# with each request: https://platform.openai.com/docs/guides/gpt/chat-completions-api

while True:
    prompt = input("Prompt ('q' to quit, 'f' to read from file.): ")
    if prompt == "q":
        break

    if prompt == "f":
        # Get the name of the newest file in PROMPT_FOLDER
        newest_file = max(glob.glob(os.path.join(PROMPT_FOLDER, "*.md")), key=os.path.getctime)

        if newest_file:
            filename = input(f"Filename (default '{newest_file}'): ")
            filename = os.path.join(PROMPT_FOLDER, filename) if filename else newest_file
        else:
            filename = input("Filename: ")
            filename = os.path.join(PROMPT_FOLDER, filename)

        try:
            with open(filename, "r") as f:
                prompt = f.read()
        except FileNotFoundError:
            print("File not found.")
            continue

    print("sending...")
    response = openai.chat.completions.create(
        model=MODEL, messages=[{"role": "user", "content": prompt}]
    ).to_dict()

    transdata = {
        "request": {
            "prompt": prompt,
        },
        "response": response,
    }

    fname = f"response{time.time_ns()}.yaml"
    yaml.dump(
        transdata,
        open(os.path.join(OUTPUT_FOLDER, fname), "w"),
        indent=4,
        Dumper=yaml.SafeDumper,
    )

    print()
    # print(response.keys())
    message = response["choices"][0]["message"]
    print("role:", message.get("role", "None"))
    print("content:", message.get("content", "No content"))
    print()
    print()
