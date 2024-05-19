from pathlib import Path
import os

from PIL import Image, ExifTags
from sanic import Sanic
from sanic.response import text, json

from dalle_functions import get_image_from_prompt


app = Sanic("DALL-EChatbot")

app.static('/', './templates/homepage.html', name="homepage")

@app.post("prompt")
async def prompt(request):
    #   Take a prompt, send to OpenAI.
    #   Show the prompt and the response.
    #   Display the input box at the bottom, with the responses in a frame above.
    # Return the body of the request as text. Remember to convert it from Bytes to str.
    prompt = request.body.decode()
    image = get_image_from_prompt(prompt)
    return text("/output/img/"+image)

@app.get("history.json")
async def history(request):
    # Return the chat history as a JSON object.
    # Get the 10 most recent images in the image output folder
    image_folder = "../output/images"
    images = sorted(Path(image_folder).glob("*.png"), key=lambda f: os.path.getmtime(str(f)))[-10:]

    outp = []
    for image in images:
        img = Image.open(os.path.join(image))
        outp.append({"prompt": img.getexif()[ExifTags.Base.ImageDescription.value][9:-1], "filename": str(image.name)})
    return json(outp)

app.static('/output/img', '../output/images', name="images")
