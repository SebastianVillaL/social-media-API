from jose import jwt, JWTError
from datetime import datetime, timedelta

#SECRET_KEY (Provides integrity to tokens, resides on the server only)
SECRET_KEY = "2a3d6e64ad97ef992b7b3262d0bb1dd733d81a60cb70796a93241bd520d7993d"

#Algorithm HS256
ALGORITHM = "HS256"

#Expiration time of the token
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
