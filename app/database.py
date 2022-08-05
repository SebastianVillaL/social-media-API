#Here is the code that manages all connections to the postgres database
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#URL -> 'posgresql://<username>:<password>@<ip_address/hostname>/<database_name>'
SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:root@localhost/fastapi'  

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

#This creates a Session to the database, send SQL statements, and close the session
def get_db():
	db = SessionLocal()
	try:
		yield db
	finally:
		db.close
