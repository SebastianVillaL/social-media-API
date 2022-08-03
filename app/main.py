from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body #Allows to extract data from the Body of a POST Request
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time

app = FastAPI() #Instance of FastAPI saved in the variable app

class Post(BaseModel): #This is a schema(to format our posts with the following criteria"
	title: str
	content: str
	published: bool = True
	rating: Optional[int] = None


while True:
	try:
		conn = psycopg2.connect(host='localhost', database='fastapi', 
								user='postgres', password='root', cursor_factory=RealDictCursor)
		cursor = conn.cursor()
		print("Database connection was succesfull!")
		break
	except Exception as error:
		print("Connecting to database failed")
		print("Error: ", error)
		time.sleep(10)
	
#This is just to store the posts as dictionaries on a list, no database yet	
my_posts = [{'title': 'title of post 1', 'content': 'content of post 1', 'id': 1},
			{'title': 'favorite foods', 'content': 'i like pizza', 'id': 2}]

#just a function to find the id on the list
def find_post(id):
	for p in my_posts:
		if p["id"] == int(id):
			return p
#just a function to find the index on the list
def find_index_post(id):
	for index, item in enumerate(my_posts):
		if item['id'] == id:
			return index

@app.get("/")
async def home():
	return {"message": "Welcome to my API"}


#Here starts the posts CRUD operations

@app.get("/posts")
def get_posts():
	return {"data": my_posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
#This receives the Body of a POST request, then stores on variable post
def create_posts(post: Post):
	post_dict = post.dict()
	post_dict['id'] = randrange(0, 10000000)
	my_posts.append(post_dict)
	return {"data": my_posts}


@app.get("/posts/{id}") #the {id} is a 'path parameter', fastAPI will extract the id(as a str)
def get_post(id: int, response: Response):
	post = find_post(id)
	if not post:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
							detail=f'post with id {id} was not found')
	return {"post_detail": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int): #deleting post (for now on a list)
	index = find_index_post(id)
	if index == None:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
			  				detail=f"post with id: {id} does not exist")
	my_posts.pop(index)
	return {'message': 'Post was succesfully deleted'} 


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
	index = find_index_post(id)
	if index == None:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
			  				detail=f"post with id: {id} does not exist")
	post_dict = post.dict()
	post_dict['id'] = id
	my_posts[index] = post_dict
	return {'data': post_dict}
