from sqlalchemy import create_engine, Column, String, Integer 
from sqlalchemy.orm import DeclarativeBase, Session 

conn = create_engine('postgresql://postgres:pulli@localhost:4569/Users')

def connection():
    if conn:
        try:
            print('connected')
        except Exception as e:
            print(e)
            
class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "Users"
    name = Column(String, nullable=False)
    mail = Column(String, nullable=False, primary_key=True)
    password = Column(String, nullable=False)
    age = Column(Integer, nullable=True)
    
db = Session(conn)
User.metadata.create_all(conn)