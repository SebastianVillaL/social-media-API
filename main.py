from fastapi import FastAPI
from fastapi.params import Body #Allows to extract data from the Body of a POST Request
from pydantic import BaseModel
from typing import Optional
from random import randrange

app = FastAPI()

class Post(BaseModel): #This is a schema(to format our posts with the following criteria"
	title: str
	content: str
	published: bool = True
	rating: Optional[int] = None
	
#This is just to store the posts as dictionaries on a list, no database yet	
my_posts = [{'title': 'title of post 1', 'content': 'content of post 1', 'id': 1},
			{'title': 'favorite foods', 'content': 'i like pizza', 'id': 2}]

#just a function to find the id on the list
def find_post(id):
	for p in my_posts:
		if p["id"] == int(id):
			return p

@app.get("/")
async def root():
	return {"message": "Welcome to my API"}


#Here starts the posts CRUD operations

@app.get("/posts")
def get_posts():
	return {"data": my_posts}

@app.post("/posts")
#This receives the Body of a POST request, then stores on variable post
def create_posts(post: Post):
	post_dict = post.dict()
	post_dict['id'] = randrange(0, 10000000)
	my_posts.append(post_dict)
	return {"data": my_posts}

@app.get("/posts/{id}") #the {id} is a 'path parameter', fastAPI will extract the id(as a str)
def get_post(id: int):
	post = find_post(id)
	return {"post_detail": post}
	
