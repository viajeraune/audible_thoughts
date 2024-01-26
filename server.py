from fastapi import FastAPI, Request, Form, File, UploadFile, HTTPException, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import shutil
import base64

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

last_uploaded_file = None

# @app.get("/")
# async def main():
#     with open("templates/home.html", 'r') as file:
#         content = file.read()
#     return HTMLResponse(content)

@app.post("/upload/")
async def upload(file: UploadFile = File(...)):
    global last_uploaded_file
    try:
        file_location = f"static/temp/{file.filename}"
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        last_uploaded_file = file_location
        return {"filename": "temp/" + file.filename}
    except Exception as e:
        return {"error": str(e)}

def get_last_uploaded_file():
    return last_uploaded_file

@app.post("/")
async def root(item: Item, image_path: str = Depends(get_last_uploaded_file)):
    if image_path is None:
        return {"error": "No image has been uploaded yet."}

    try:
        with open(image_path, "rb") as image_file:
            encoded_img = base64.b64encode(image_file.read()).decode('utf-8')
        encoded_img = "data:image/jpeg;base64," + encoded_img

        print(encoded_img)
        output = replicate.run(
            "nateraw/video-llava:a494250c04691c458f57f2f8ef5785f25bc851e0c91fd349995081d4362322dd",
            input={
                "image_path": encoded_img,
                "text_prompt": "What is going on in this image? Summarize key vibes in 10 words or less."
            }
        )
        print(output)
        return {output}

    except Exception as e:
        return {"error": str(e)}
    
# async def root(item: Item):
#     print("submit button clicked")
#     test = "test data"
    
#     image_path = f"static/temp/{file.filename}"
#     with open(image_path, "rb") as image_file:
#         encoded_img = base64.b64encode(image_file.read()).decode('utf-8')

#     encoded_img = "data:image/jpeg;base64," + encoded_img

#     print(encoded_img)

#     output = replicate.run(
#         "nateraw/video-llava:a494250c04691c458f57f2f8ef5785f25bc851e0c91fd349995081d4362322dd",
#         input={
#             "image_path": encoded_img,
#             "text_prompt": "What is going on in this image? Summarize key vibes in 10 words or less."
#         }
#     )
#     print(output)

#     return {output}