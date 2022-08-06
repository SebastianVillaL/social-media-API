#Python
from typing import Optional, List
import time
#Pydantic
from pydantic import BaseModel
#Fastapi
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body #Allows to extract data from the Body of a POST Request
#Psycopg2
import psycopg2
from psycopg2.extras import RealDictCursor
#SQLAlchemy
from sqlalchemy.orm import Session
#Project files
from . import models, schemas, utils
from .database import engine, get_db

#This command creates all the tables based on the models on the models.py file
models.Base.metadata.create_all(bind=engine)

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


#Here starts the CRUD operations for the social media posts
@app.get("/posts", response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts


#This receives the Body of a POST request, validates it using the schema.Post then stores on variable post
@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.PostOut)
def create_posts(post: schemas.Post, db: Session = Depends(get_db)):

    new_post = models.Post(**post.dict()) # -> ** <- This unpacks the dictionary
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post #Using the response_model FastAPI will convert this to JSON automatically


@app.get("/posts/{id}", response_model=schemas.PostOut) #the {id} is a 'path parameter', fastAPI will extract the id(as a str)
def get_post(id: int, response: Response, db: Session = Depends(get_db)):

    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with id {id} was not found')
    return post


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)): 

    post_query = db.query(models.Post).filter(models.Post.id == id)

    if post_query.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with id {id} does not exist')

    post_query.delete(synchronize_session=False)
    db.commit()
    return {'message: Post was succesfully deleted'} 


@app.put("/posts/{id}", response_model=schemas.PostOut)
def update_post(id: int, post: schemas.Post, db: Session = Depends(get_db)):

    post_query = db.query(models.Post).filter(models.Post.id == id)
    if post_query.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")

    post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()



#Here starts the CRUD operations for the users 
@app.post("/registration", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.User, db: Session = Depends(get_db)):

    #Hash password
    user.password = hash(user.password)

    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@app.get("/users/{id}", response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):

    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'user with id {id} was not found')
    return user
