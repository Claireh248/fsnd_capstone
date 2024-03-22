import os
from sqlalchemy import Column, String, Integer, DateTime
from enum import Enum
from flask_sqlalchemy import SQLAlchemy
import json
from dotenv import load_dotenv

load_dotenv()
db = SQLAlchemy()

database_path = os.getenv("database_path")

########
#setup db

def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = os.getenv("SQLALCHEMY_TRACK_MODIFICATIONS")
    db.app = app
    db.init_app(app)
    db.create_all()
    

######

'''
Class to create enum on gender in Actor Modal
'''

class GenderChoices(Enum):
    MALE = 'MALE'
    FEMALE = 'FEMALE'
    NON_BINARY = 'NON_BINARY'
    OTHER = 'OTHER'

'''
Actor Model
    Integer id - PK
    String name
    Integer Age
    String gender
'''

class Actor(db.Model):
    __tablename__ = 'actors'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)
    gender = Column(db.Enum(GenderChoices))

    def insert(self):
        db.session.add(self)
        db.session.commit()
  
    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age, 
            'gender': self.gender.value if self.gender else None
        }

'''
Movie Model
    Integer id - PK
    String title
    Datetime Release Date
'''

class Movie(db.Model):
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    release_date = Column(db.DateTime)

    def insert(self):
        db.session.add(self)
        db.session.commit()
  
    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date 
        }





