from fastapi import FastAPI, Request, Form, File, UploadFile, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from pydantic import BaseModel
from typing import List, Optional
import requests
import replicate
import os
from dotenv import load_dotenv
import base64
import json
import io

load_dotenv()

app = FastAPI()
templates = Jinja2Templates(directory = 'templates')
app.mount("/static", StaticFiles(directory="static"), name="static")



os.environ["REPLICATE_API_TOKEN"] = os.getenv("REPLICATE_TOKEN")


##############################################
@app.get("/")
def home(request: Request):
    ''' Returns html jinja2 template render for home page form
    '''

    return templates.TemplateResponse('home.html', {
            "request": request,
        })

class Item(BaseModel):
    search: str

@app.post("/")
async def root(item: Item):
    print("submit button clicked")
    test = "test data"
    
    image_path = "static/fireplace.jpeg"
    with open(image_path, "rb") as image_file:
        encoded_img = base64.b64encode(image_file.read()).decode('utf-8')

    encoded_img = "data:image/jpeg;base64," + encoded_img

    # print(encoded_img)

    output_text = replicate.run(
        "nateraw/video-llava:a494250c04691c458f57f2f8ef5785f25bc851e0c91fd349995081d4362322dd",
        input={
            "image_path": encoded_img,
            "text_prompt": "What is going on in this image?"
        }
    )
    output = replicate.run(
        "lucataco/magnet:e8e2ecd4a1dabb58924aa8300b668290cafae166dd36baf65dad9875877de50e",
        input={
            "prompt": output_text,
            "variations": 1
        }
    )
    print(output[0])

    return {output[0]}