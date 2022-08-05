from pydantic import BaseModel

class Post(BaseModel): #This is a schema(to format our posts with the following criteria)
	title: str
	content: str
	published: bool = True
