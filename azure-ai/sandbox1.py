import logging
from pathlib import Path

import httpx
import yaml

logging.basicConfig(filename="./logs/azureai.log", level=logging.INFO)

settings = yaml.safe_load(open("settings.yaml"))

TARGET_URL = settings['target_url']
KEY = settings["key"]
API_VERSION = settings["api_version"]

uri = f"/chat/completions?api-version={API_VERSION}"
url = f"{TARGET_URL}{uri}"

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {KEY}",
    "extra-parameters": "error"
}


messages = [
    {"role": "system", "content": Path('system_prompt.txt').read_text()},
]

payload = {
    "messages": messages,
}

while True:
    prompt = input("You ('q' to quit): ")

    if prompt == "q":
        break

    payload["messages"].append({"role": "user", "content": prompt})
    
    resp = httpx.post(url=url, headers=headers, json={"messages": messages}, timeout=30)

    logging.info("Status code %s" % resp.status_code)
    logging.info(resp.text)
    print(resp.json()["choices"][0]["message"]["content"])