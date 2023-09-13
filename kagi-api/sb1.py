
import os

from dotenv import load_dotenv
import requests

load_dotenv()
BASE_URL = os.getenv("BASE_URL")
API_TOKEN = os.getenv("API_TOKEN")
print(BASE_URL, API_TOKEN)

while True:
    print()
    query = input("Enter a query or 'q' to quit: ")
    if query == "q":
        break

    data = {
        "query": query,
        "cache": False,
    }
    headers = {'Authorization': f'Bot {API_TOKEN}'}

    response = requests.post(BASE_URL, headers=headers, json=data)
    
    if response.status_code!= 200:
        print("EPIC FAIL!", response.status_code, response.reason)    
        break

    rspdata = response.json()

    #print(rspdata)
    #print("Query: "+ query)
    #print("API Balance: $"+str(rspdata['meta']['api_balance']))
    print()
    print(rspdata['data']['output'])
    print("Reference count:", len(rspdata['data'].get('references', [])))