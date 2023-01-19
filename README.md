# Social media FastAPI

### Hey! I'm just created a FastAPI Social Media beginner project.

### How it work?

#### 1) Install PostgreSQL on your computer
#### 2) Install the follow libraries:

*pip install fastapi*

*pip install "uvicorn[standard]"*

*pip install sqlalchemy*

*pip install "python-jose[cryptography]"*

*pip install "passlib[bcrypt]"*


#### Run the app with the following command: uvicorn app.main:app
#### If you need debug mode: uvicorn app.main:app --reload

##### Use Postman, Insomnia or Terminal / Command for CRUD Operations
##### You can see the path in FastAPI docs (localhost:8000/docs) >> at default

#### Always change this line in app/database.py (it's only a dummy DB data):
##### SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:root@localhost/socialmedia'
##### where 'database_type://username:password@host/db_name'


## Have fun!
