from pydantic import BaseModel

class User(BaseModel):
    name: str
    mail: str
    password: str
    age: int
