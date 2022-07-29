from fastapi import FastAPI
from fastapi.params import Body #Allows to extract data from the Body of a POST Request

app = FastAPI()

@app.get("/")
async def root():
	return {"message": "Welcome to my API"}

@app.get("/posts")
def get_posts():
	return {"data": "This are your posts"}

@app.post("/createposts")
#This receives the Body of a POST request, converts to python dict, then stores on variable payLoad
def create_posts(payLoad: dict = Body(...)):
	print(payLoad)
	return {"new_post": f"title: {payLoad['title']} content: {payLoad['content']}"}
