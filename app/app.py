from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from app.Validation.user import User
from app.db.db import connection
from app.db.db import db, User as user_schema
from sqlalchemy import select
from pydantic import BaseModel

app = FastAPI()
connection()

arr = [{"id": 1, "name": "tharun"}, {"id": 2, "name": "ram"}, {"id": 3, "name": "sanjeev"}]

@app.get('/')
def root():
    return {"mssg": "Helloww, World!!"}

@app.get('/items')
def get_items():
    return db.query(user_schema).all()

class Test(BaseModel):
    text: str
    syn: str

@app.post('/create')
def create_user(payload: Test):
    val = payload.mail
    exists = db.execute(select(user_schema).where(user_schema.mail == val)).first()
    if exists:
        # return Response(content='Already exists!!, Please create a new one!!', status_code=409, media_type='plain/text')
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Already exists!!, Please create a new one!!')
    else:
        # print(**payload.model_dump())
        new_user = user_schema(name = payload.name, mail = payload.mail, password = payload.password, age = payload.age)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return Response(content='User added!!', status_code=201, media_type='plain/text')
    
@app.get('/{name}')
def get_id(name: str): 
    user = db.query(user_schema).filter(user_schema.name == name).first()
    if user:
        return user, Response(status_code=status.HTTP_302_FOUND)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

@app.get('/fault')
def fault_eg():
    raise HTTPException.status_code(status_code=500)
    

@app.post('/test')
def post_request(payload : dict = Body(...)):
    print(payload)
    return {"mssg": "successful"}

@app.post('/create', status_code=status.HTTP_201_CREATED)
def create_user(data: User):
    print(f'name: {data.name} password: {data.password}')
