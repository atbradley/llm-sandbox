import os
import time

from dotenv import load_dotenv
from io import BytesIO
import openai
from PIL import Image, ExifTags
import requests

load_dotenv()

openai.api_key = os.getenv("API_KEY")

def get_image_from_prompt(prompt, size:int=1024) -> str:
    """
    Gets an image from DALL-E based on the prompt, and saves it to a file with
    the prompt saved in the Image Description exif tag. Returns the filename. 
    """
    sz = str(size) + "x" + str(size)

    response = openai.Image.create(
        prompt=prompt,
        n=1,
        size=sz,
    )

    imgrs = requests.get(response['data'][0]['url'])

    if imgrs.status_code != 200:
        raise Exception(f"Failed to get image from prompt: {prompt}")

    imgdata = imgrs.content

    with open("image.png", "wb") as f:
        f.write(imgdata)
    
    imgio = BytesIO(imgdata)
    img = Image.open(imgio)
    exif = img.getexif()
    exif[ExifTags.Base.ImageDescription.value] = f'Prompt: "{prompt}"'

    fname = f"dalle-{time.time_ns()}.png"
    img.save(f"images/{fname}", exif=exif)

    return fname

if __name__ == "__main__":
    prompt = input("Prompt? ")
    get_image_from_prompt(prompt, 256)
