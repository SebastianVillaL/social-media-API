#Here is the code that manages all connections to the postgres database
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

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



# This is to set a connection to the fastapi database on the postgres server
# while True:
    # try:
        # conn represents the connection to the database
        # conn = psycopg2.connect(host='localhost', database='fastapi',
                                # user='postgres', password='root',
                                # cursor_factory=RealDictCursor)
        # cursor = conn.cursor()
        # print("Database connection was succesfull!")
        # break
    # except Exception as error:
        # print("Connecting to database failed")
        # print("Error: ", error)
        # time.sleep(10)
