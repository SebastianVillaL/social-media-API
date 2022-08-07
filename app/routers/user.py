#Python
from typing import List
#Fastapi
from fastapi import Response, status, HTTPException, Depends, APIRouter
from fastapi.params import Body #Allows to extract data from the Body of a POST Request
#SQLAlchemy
from sqlalchemy.orm import Session
#Project files
from .. import models, schemas
from ..database import get_db


router = APIRouter()


#Here starts the CRUD operations for the users
@router.post("/registration", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.User, db: Session = Depends(get_db)):

    #Hash password
    user.password = hash(user.password)

    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.get("/users/{id}", response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):

    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'user with id {id} was not found')
    return user