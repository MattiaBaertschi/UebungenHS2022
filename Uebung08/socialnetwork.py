import uvicorn

from fastapi import FastAPI, Depends, status , Form, Request, Cookie
from fastapi.responses import RedirectResponse, HTMLResponse

#Importieren der Bibliotheken für Login
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_login import LoginManager
from fastapi_login.exceptions import InvalidCredentialsException

#Importieren der Bibliotheken für DB
import databases
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData
from fastapi.templating import Jinja2Templates


#Aufsetzen der DB
DATABASE_URL = "sqlite:///./blogs.db"

database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()

blogs = sqlalchemy.Table(
    'blogs',
    metadata,
    sqlalchemy.Column('id', sqlalchemy.Integer, primary_key = True),
    sqlalchemy.Column('username', sqlalchemy.String),
    sqlalchemy.Column('blogtitel', sqlalchemy.String),
    sqlalchemy.Column('blogtext', sqlalchemy.String),
)

engine = sqlalchemy.create_engine(
    DATABASE_URL, connect_args={"check_same_thread":False}
       
)
metadata.create_all(engine)


#App Starten
app = FastAPI()
templates = Jinja2Templates(directory='templates/')

def get_id(username):
    count = 0
    for value in list(DB.values()):
        count += 1
        if value == username:
            user = list(DB.keys())[count-1]
            return user


#Verbindung mit DB
@app.on_event("startup")
async def startup():
    print("verbinde DB")
    await database.connect()

#Verbindung mit DB trennen
@app.on_event("shutdown")
async def shutdown():
    print("trenne DB")
    await database.disconnect()


#Login von div. Benuzern
manager = LoginManager("abcd", token_url="/auth/login", use_cookie=True)
manager.cookie_name = "ch.fhnw.testapp_asdf"

DB = {  "user1": {"name": "Hans Muster",
                "email": "hanswurst@gmail.com",
                "passwort":"12345",
                },
        "user2": {"name": "Alexandra Meier",
                "email": "ameier@gmx.net",
                "passwort":"pass",
                }
        }

@manager.user_loader()
def load_user(username: str):
    user = DB.get(username) #DB[username] würde das selbe machen aber wenn der user nicht existiert würde das Programm beendet werden, was nicht gut währe
    return user
    

@app.post("/auth/login")
def login(data: OAuth2PasswordRequestForm = Depends()):     #bei allen Logins die es gibt sollte man "username" als name und "password" als passwort nemen damit diese als solche erkannt werden
    username = data.username
    password = data.password #hier werden pw und username vom fromulag geholt
    user = load_user(username)

    if not user:
        raise InvalidCredentialsException
    if user['passwort'] != password:
        raise InvalidCredentialsException
    
    access_token = manager.create_access_token(
        data = {"sub": username}
    )
    
    resp = RedirectResponse(url="/new", status_code=status.HTTP_302_FOUND)
    manager.set_cookie(resp,access_token)



    return resp

#read
@app.get("/login")
def login():
    file = open("templates/login.html", encoding="utf-8")
    data = file.read()
    file.close()
    return HTMLResponse(content=data) 



#create
@app.post("/new")
async def post_blog(blogtitel=Form(), blogtext=Form(), user=Depends(manager)):
    username = get_id(user)
    query = blogs.insert().values(username=username ,blogtitel=blogtitel, blogtext = blogtext)
    myid = await database.execute(query)

    # print(f"der benuzer ist: {benuzer} myid={myid } blogtitel={blogtitel}")
    return {"id": myid, "blogtitel":blogtitel,"blogtext":blogtext, "user_id":username}
    


@app.get("/new", response_class=HTMLResponse)
async def create_blog(request:Request, user=Depends(manager)):

    return templates.TemplateResponse('new.html',
    context={'request':request})


@app.post("/users/{user_id}")
async def get_username(user_id: str):
    b = blogs.select()
    r = engine.execute(b)

    print(blogs.get_children())

    L = []

    for row in r:
        L.append(str(row))

    
    return {str(L)}


uvicorn.run(app, host="127.0.0.1", port=8000)