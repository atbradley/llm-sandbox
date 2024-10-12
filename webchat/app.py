import openai
from sanic import Sanic
from sanic.response import json

from settings import *

app = Sanic("BasicSanicApp")

app.static("/", "front/index.html", name="index")
app.static("/static", "front", name="static")

llm = openai.OpenAI(
    api_key=api_key,
    base_url=base_url,
)

@app.post("/chat")
async def chat(request):
    response = llm.chat.completions.create(
        model="Mistral-Nemo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
        ]+request.json,
    ).to_dict()

    # Remember not to return the system message.
    resp = request.json + [response['choices'][0]['message']]
    print(resp)
    return json(resp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7000, debug=True, auto_reload=True)