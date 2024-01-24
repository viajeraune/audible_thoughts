from fastapi import FastAPI, Request, Form, File, UploadFile, HTTPException
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import List, Optional
from fastapi.responses import HTMLResponse
import requests
import replicate
import os
from dotenv import load_dotenv

import base64
import random
import json

load_dotenv()

app = FastAPI()
templates = Jinja2Templates(directory = 'templates')


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

