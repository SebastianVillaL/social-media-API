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
from .routers import post, user

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
	
#Instance of FastAPI saved in the variable app
app = FastAPI()
app.include_router(post.router)
app.include_router(user.router)

#This is the home of the API
@app.get("/")
async def home():
    return {"message": "Welcome to my API"}
