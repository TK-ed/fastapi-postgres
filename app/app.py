from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from app.Validation.user import User
from app.db.db import connection
from app.db.db import db, User as user_schema

app = FastAPI()
connection()

arr = [{"id": 1, "name": "tharun"}, {"id": 2, "name": "ram"}, {"id": 3, "name": "sanjeev"}]

@app.get('/')
def root():
    return {"mssg": "Helloww, World!!"}

@app.get('/items')
def get_items():
    return db.query(user_schema).all()


@app.post('/create')
def create_user(payload: User):
    val = payload.mail
    # exists = db.execute(select(user_schema).where(user_schema.mail == val)).first()
    exists = db.query(user_schema).filter(user_schema.mail == val).first()
    if exists:
        # return Response(content='Already exists!!, Please create a new one!!', status_code=409, media_type='plain/text')
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Already exists!!, Please create a new one!!')
    else:
        # new_user = user_schema(name = payload.name, mail = payload.mail, password = payload.password, age = payload.age)
        new_user = user_schema(**payload.model_dump())
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user, Response(content='User added!!', status_code=status.HTTP_201_CREATED, media_type='plain/text')
    
@app.get('/{name}')
def get_id(name: str): 
    user = db.query(user_schema).filter(user_schema.name == name).first()
    if user:
        return user, Response(status_code=status.HTTP_302_FOUND)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

@app.delete('/{name}', status_code = status.HTTP_200_OK)
def delete_user(name: str):
    user = db.query(user_schema).filter(user_schema.name == name).first()
    if user:
        db.delete(user)
        db.commit()
        return user
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found!!')

@app.put('/{name}', status_code = status.HTTP_202_ACCEPTED)
def update_user(name: str, alt: str):
    try:
        user = db.query(user_schema).filter(user_schema.name == name).first()
        user.name = alt
        return user
    except Exception as e:
        return e
    
 

@app.post('/test')
def post_request(payload : dict = Body(...)):
    print(payload)
    return {"mssg": "successful"}

@app.post('/create', status_code=status.HTTP_201_CREATED)
def create_user(data: User):
    print(f'name: {data.name} password: {data.password}')
