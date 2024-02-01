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

@app.post("/upload/")
async def upload(file: UploadFile = File(...)):
    global last_uploaded_file
    try:
        file_location = f"static/temp/{file.filename}"
        with open(file_location, "wb") as buffer:
            print(0)
            shutil.copyfileobj(file.file, buffer)
            print(1)
        last_uploaded_file = file_location
        print(2)
        return {"filename": "temp/" + file.filename}
    except Exception as e:
        return {"error": str(e)}

def get_last_uploaded_file():
    return last_uploaded_file

@app.post("/", response_class=HTMLResponse)
async def root(request: Request, item: Item, file_path: str = Depends(get_last_uploaded_file)):
    if file_path is None:
        return {"error": "No file has been uploaded yet."}

    try:
<<<<<<< Updated upstream
        #with open(image_path, "rb") as image_file:
        #    encoded_img = base64.b64encode(image_file.read()).decode('utf-8')
        #encoded_img = "data:image/jpeg;base64," + encoded_img

        # print(encoded_img)
        print(image_path)
        output_text = replicate.run(
            "nateraw/video-llava:a494250c04691c458f57f2f8ef5785f25bc851e0c91fd349995081d4362322dd",
            input={
                #"image_path": encoded_img,
                "video_path": image_path,
                "text_prompt": "What is going on in this image? Summarize key vibes in 10 words or less."
            }
        )
        output = replicate.run(
        "lucataco/magnet:e8e2ecd4a1dabb58924aa8300b668290cafae166dd36baf65dad9875877de50e",input={
            "prompt": "high quality environmental background ambient sound and music for " + output_text,
            "variations": 1
        }
    )
=======
        # Determine file type (image or video) based on file extension
        if file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
            mime_type = "image/jpeg"  # Default for most images, adjust if using GIF or PNG
            with open(file_path, "rb") as file:
                encoded_file = base64.b64encode(file.read()).decode('utf-8')
            encoded_file = f"data:{mime_type};base64," + encoded_file
            # Handle as image
            # Use encoded_file in your image processing logic here
        elif file_path.lower().endswith(('.mp4', '.mov', '.avi')):
            mime_type = "video/mp4"  # Adjust based on actual video format
            with open(file_path, "rb") as file:
                encoded_file = base64.b64encode(file.read()).decode('utf-8')
            encoded_file = f"data:{mime_type};base64," + encoded_file
            # Handle as video
            # Use encoded_file in your video processing logic here
        else:
            return {"error": "Unsupported file type."}

        # Example of using encoded_file with replicate (adjust according to actual usage)
        output_text = replicate.run(
            "nateraw/video-llava:a494250c04691c458f57f2f8ef5785f25bc851e0c91fd349995081d4362322dd",
            input={
                "video_path": encoded_file,  # Adjust the parameter name as needed
                "text_prompt": "What is going on in this image or video? Reduce noise, make sound clear and crisp."
            }
        )
        output = replicate.run(
            "lucataco/magnet:e8e2ecd4a1dabb58924aa8300b668290cafae166dd36baf65dad9875877de50e",
            input={
                "prompt": output_text,
                "variations": 1
            }
        )
>>>>>>> Stashed changes

        print(output_text)
        print(output[0])
        audio_link = output[0]

        return templates.TemplateResponse("result.html", {
            "request": request, 
            "output_text": output_text,
            "audio_link": audio_link
        })
    
    except Exception as e:
        return {"error": str(e)}

# @app.post("/", response_class=HTMLResponse)
# async def root(request: Request, item: Item, image_path: str = Depends(get_last_uploaded_file)):
#     if image_path is None:
#         return {"error": "No image has been uploaded yet."}

#     try:
#         with open(image_path, "rb") as image_file:
#             encoded_img = base64.b64encode(image_file.read()).decode('utf-8')
#         encoded_img = "data:image/jpeg;base64," + encoded_img

#         # print(encoded_img)
#         output_text = replicate.run(
#             "nateraw/video-llava:a494250c04691c458f57f2f8ef5785f25bc851e0c91fd349995081d4362322dd",
#             input={
#                 "image_path": encoded_img,
#                 "text_prompt": "What is going on in this image? Summarize key vibes in 10 words or less."
#             }
#         )
#         output = replicate.run(
#         "lucataco/magnet:e8e2ecd4a1dabb58924aa8300b668290cafae166dd36baf65dad9875877de50e",input={
#             "prompt": output_text,
#             "variations": 1
#         }
#     )

#         print(output_text)
#         print(output[0])
#         audio_link = output[0]
#         # return {output[0]}

#         return templates.TemplateResponse("result.html", {
#             "request": request, 
#             "output_text": output_text,
#             "audio_link": audio_link
#         })
    
#     except Exception as e:
#         return {"error": str(e)}


