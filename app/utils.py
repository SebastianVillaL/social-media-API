#Passlib
from passlib.context import CryptContext

#This is to set the defauls hashing algorithm bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash(password: str):
    return pwd_context.hash(password)

def verify(plain_pwd, hashed_pwd):
    return pwd_context.verify(plain_pwd, hashed_pwd)
