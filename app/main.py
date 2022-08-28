#Fastapi
from fastapi import FastAPI
#Project files
from . import models
from .database import engine
from .routers import post, user, auth


#This command creates all the tables based on the models on the models.py file
models.Base.metadata.create_all(bind=engine)


#Instance of FastAPI saved in the variable app
app = FastAPI()
#This will get the router object from the .routers folder
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)


#This is the home of the API
@app.get("/")
async def home():
    return {"message": "Welcome to my API"}
