#Python
from typing import List
#Fastapi
from fastapi import Response, status, HTTPException, Depends, APIRouter
from fastapi.params import Body #Allows to extract data from the Body of a POST Request
#SQLAlchemy
from sqlalchemy.orm import Session
#Project files
from .. import models, schemas, oauth2
from ..database import get_db


router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)


#Here starts the CRUD operations for the social media posts
@router.get("/", response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts


@router.get("/myposts", response_model=List[schemas.PostOut])
def get_my_posts(db: Session = Depends(get_db),
                 current_user: int = Depends(oauth2.get_current_user)):

    my_posts = db.query(models.Post).filter(models.Post.user_id == current_user.id).all()
    return my_posts


#This receives the Body of a POST request, validates it using the schema.Post then stores on variable post
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostOut)
def create_posts(post: schemas.Post, db: Session = Depends(get_db),
                 current_user :int = Depends(oauth2.get_current_user)):
    new_post = models.Post(user_id=current_user.id, **post.dict()) # -> ** <- This unpacks the dictionary
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post #Using the response_model FastAPI will convert this to JSON automatically


@router.get("/{id}", response_model=schemas.PostOut) #the {id} is a 'path parameter', fastAPI will extract the id(as a str)
def get_post(id: int, response: Response, db: Session = Depends(get_db)):

    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with id {id} was not found')
    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db),
                current_user :int = Depends(oauth2.get_current_user)):

    post_query = db.query(models.Post).filter(models.Post.id == id)

    if post_query.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with id {id} does not exist')

    if post_query.first().user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")

    post_query.delete(synchronize_session=False)
    db.commit()
    return {'message: Post was succesfully deleted'}


@router.put("/{id}", response_model=schemas.PostOut)
def update_post(id: int, post: schemas.Post, db: Session = Depends(get_db),
                current_user :int = Depends(oauth2.get_current_user)):

    post_query = db.query(models.Post).filter(models.Post.id == id)

    if post_query.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")

    if post_query.first().user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")

    post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()
