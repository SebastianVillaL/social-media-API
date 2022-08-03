from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body #Allows to extract data from the Body of a POST Request
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time


class Post(BaseModel): #This is a schema(to format our posts with the following criteria)
	title: str
	content: str
	published: bool = True


#This is to set a connection to the fastapi database on the postgres server
while True:
	try:
		#conn represents the connection to the database
		conn = psycopg2.connect(host='localhost', database='fastapi', 
								user='postgres', password='root', cursor_factory=RealDictCursor)
		cursor = conn.cursor()
		print("Database connection was succesfull!")
		break
	except Exception as error:
		print("Connecting to database failed")
		print("Error: ", error)
		time.sleep(10)
	

app = FastAPI() #Instance of FastAPI saved in the variable app
#This is the home of the API
@app.get("/")
async def home():
	return {"message": "Welcome to my API"}


#Here starts the posts CRUD operations

@app.get("/posts")
def get_posts():

	cursor.execute("""SELECT * FROM posts """)
	posts = cursor.fetchall()

	return {"data": posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
#This receives the Body of a POST request, then stores on variable post
def create_posts(post: Post):

	cursor.execute(""" INSERT INTO posts (title, content, published) VALUES(%s, %s, %s) 
					RETURNING * """, (post.title, post.content, post.published))
	new_post = cursor.fetchone()
	conn.commit()

	return {"data": new_post}


@app.get("/posts/{id}") #the {id} is a 'path parameter', fastAPI will extract the id(as a str)
def get_post(id: int, response: Response):

	cursor.execute(""" SELECT * FROM posts WHERE id = %s """, (str(id)))
	post = cursor.fetchone()

	if not post:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
							detail=f'post with id {id} was not found')
	return {"post_detail": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int): 

	cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING * """, (str(id)))
	deleted_post = cursor.fetchone()
	conn.commit()

	if deleted_post == None:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
							detail=f'post with id {id} does not exist')
	return {'message: Post was succesfully deleted'} 


@app.put("/posts/{id}")
def update_post(id: int, post: Post):

	cursor.execute(""" UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s 
					RETURNING * """,
					(post.title, post.content, post.published, str(id)))
	updated_post = cursor.fetchone()
	conn.commit()

	if updated_post == None:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
			  				detail=f"post with id: {id} does not exist")
	return {'data': updated_post}
