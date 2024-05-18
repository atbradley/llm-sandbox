import os
import time

from dotenv import load_dotenv
import requests
import yaml

load_dotenv()
BASE_URL = os.getenv("SUMMARIZER_URL")
API_TOKEN = os.getenv("API_TOKEN")
OUTPUT_FOLDER = os.getenv("OUTPUT_FOLDER")
engine = os.getenv("DEFAULT_SUMMARIZER")
summary_type = os.getenv("SUMMARY_TYPE")
# print(BASE_URL, API_TOKEN, engine, summary_type)

summarizer_options = {
    "cecil": "Friendly, descriptive, fast summary",
    "agnes": "Formal, technical, analytical summary",
    "daphne": "Informal, creative, friendly summary",
    "muriel": "Best-in-class summary using our enterprise-grade model ($1/request)",
}

summary_type_options = ["summary", "takeaway"]


while True:
    print()
    print(f"current summarizer: {engine} ({summarizer_options[engine]})")
    print(f"summary type: {summary_type} (options: {summary_type_options})")

    url = input(
        "Enter a URL, 'e' to change engine, 't' to change summary type, or 'q' to quit: "
    )
    if url == "q":
        break
    elif url == "e":
        print("summarizer options:")
        for eng, desc in summarizer_options.items():
            print(f"  {eng} ({desc})")
        neweng = input("Enter a new summarizer: ")

        newengfilter = filter(lambda x: x[0] == neweng[0], summarizer_options.keys())
        try:
            engine = next(newengfilter)
        except StopIteration:
            print(f"Invalid summarizer: {neweng}")
        continue
    elif url == "t":
        typefilter = filter(lambda x: x != summary_type, summary_type_options)
        summary_type = next(typefilter)
        continue
    elif not url.startswith("http"):
        print(f"Invalid URL: {url}")
        continue

    data = {
        "url": url,  # "text" is also an option.
        "engine": engine,
        "summary_type": summary_type,
        "cache": True,
        "target_language": "EN",
    }
    headers = {"Authorization": f"Bot {API_TOKEN}"}

    response = requests.post(BASE_URL, headers=headers, json=data)

    if response.status_code != 200:
        print("EPIC FAIL!", response.status_code, response.reason)
        break

    rspdata = response.json()

    # print(rspdata)
    # print("Query: "+ query)
    # print("API Balance: $"+str(rspdata['meta']['api_balance']))
    print()
    # print(rspdata)
    print(rspdata["data"]["output"])
    print(
        "Token count:",
        rspdata["data"]["tokens"],
        "API Balance: $" + str(rspdata["meta"]["api_balance"]),
    )

    fname = f"summary{time.time_ns()}.yaml"
    yaml.dump(
        rspdata,
        open(os.path.join(OUTPUT_FOLDER, fname), "w"),
        indent=4,
        Dumper=yaml.SafeDumper,
    )
