from fastapi import FastAPI
from fastapi.params import Body #Allows to extract data from the Body of a POST Request
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

class Post(BaseModel): #This is a schema(to format our posts with the following criteria"
	title: str
	content: str
	published: bool = True
	rating: Optional[int] = None
	

@app.get("/")
async def root():
	return {"message": "Welcome to my API"}

@app.get("/posts")
def get_posts():
	return {"data": "This are your posts"}

@app.post("/posts")
#This receives the Body of a POST request, then stores on variable payLoad
def create_posts(payLoad: Post):
	return {"data": "new post"}
