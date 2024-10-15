import json
import os
import time

from dotenv import load_dotenv
import httpx
import yaml

load_dotenv()
BASE_URL = os.getenv("BASE_URL")
API_TOKEN = os.getenv("API_TOKEN")
OUTPUT_FOLDER = os.getenv("OUTPUT_FOLDER")

while True:
    print()
    query = input("Enter a query or 'q' to quit: ")
    if query == "q":
        break

    data = {
        "query": query,
        "cache": False,
    }
    headers = {"Authorization": f"Bot {API_TOKEN}"}

    response = httpx.post(BASE_URL, headers=headers, json=data, timeout=30)

    if response.status_code != 200:
        print("EPIC FAIL!", response.status_code, response.reason)
        break

    rspdata = response.json()

    # print(rspdata)
    # print("Query: "+ query)
    print("API Balance: $" + str(rspdata["meta"]["api_balance"]))
    print()
    print(rspdata["data"]["output"])
    print("Reference count:", len(rspdata["data"].get("references", [])))

    filename = f"query{time.time_ns()}.yaml"
    jsondata = json.dumps(rspdata, indent=4)
    yamldata = json.loads(jsondata)
    yaml.dump(
        yamldata,
        open(os.path.join(OUTPUT_FOLDER, filename), "w"),
        indent=4,
        Dumper=yaml.SafeDumper,
    )
