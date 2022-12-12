from database import Base




from textwrap import shorten
from unicodedata import name
from database import Base, db


from sqlalchemy import Table, Column, Integer, String, Text
import uuid
import json
import sqlalchemy
from sqlalchemy.types import TypeDecorator
from database import db
from uuid import uuid4

import json
import sqlalchemy
from sqlalchemy.types import TypeDecorator
from sqlalchemy import inspect
from schemas.patient import Patient as PatientSchema





SIZE = 5120

class TextPickleType(TypeDecorator):

    impl = sqlalchemy.Text(SIZE)

    def process_bind_param(self, value, dialect):
        if value is not None:
            value = json.dumps(value)

        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            value = json.loads
        return value



#generate uuid
def generate_uuid():
    return str(uuid.uuid4())


class Patient(Base):
    __tablename__ = 'patients'

    uuid = Column(String(150),primary_key=True,default=generate_uuid , name="uuid")
    id = Column('id', String(20))
    name = Column('name', String(20))
    pregnancies = Column('pregnancies', Integer)
    glucose = Column('glucose', Integer)
    bloodpressure = Column('bloodpressure', Integer)
    skinthickness = Column('skinthickness', Integer)
    insulin = Column('insulin', Integer)
    bmi = Column('bmi', Integer)
    dpf = Column('dpf', Integer)
    age = Column('age', Integer)
    # outcome = Column('outcome', Integer)

    #init method

    def __init__(self, *,uuid:str = generate_uuid(),id:str = "",name:str = "", pregnancies:int = 1, glucose:int=1, bloodpressure:int=1, skinthickness:int=1, insulin:int=1, bmi:int=30.0, dpf:int=100.0, age:int=30):

        print("uuid:", uuid)
        print(len(uuid))

        self.uuid = uuid
        self.id = id
        self.name = name
        self.pregnancies = pregnancies
        self.glucose = glucose
        self.bloodpressure = bloodpressure
        self.skinthickness = skinthickness
        self.insulin = insulin
        self.bmi = bmi
        self.dpf = dpf
        self.age = age
        # self.outcome = outcome

        print(self.__dict__)


        self.model = Patient
        self.schema = PatientSchema

   
     #METHODS TO QUERY DB

  
    def __repr__(self):
        return '<Patient {}>'.format(self.name)

    
    def get_all(self):
        try:
            db_objects = db.query(self.model).all() # The actual query
            if db_objects:
                return db_objects
            else:
                print(f"No {self.model} was found!")
                return None
        except Exception as e:
            print(f"Error while getting all {self.model}s.")
            print(e)
            db.rollback()


    


    def get_by(self, **kwargs):
        try:
            db_object = db.query(self.model).filter_by(**kwargs).first()
            if db_object:
                return db_object
            else:
                print(f"No {self.model} was found with the given arguments!")
                return None
        except Exception as e:
            print(f"Error while getting {self.model} by {kwargs}.")
            print(e)
            db.rollback()
            

    def create(self, obj: PatientSchema):
        try:
            obj_in_db = self.get_by(name=obj.name)
            if obj_in_db is None:
                print(f"No {self.model} was found with name {obj.name}!")

                new_obj = self.model(**obj.dict())
                print(new_obj)
                db.add(new_obj)
                db.commit()

                print(f"{self.model} has been added to the database!")
                obj = self.schema.from_orm(new_obj)
                # insp = inspect(obj)
                # insp.persistent
            else:
                obj = None
                print(f"A {self.model} already exists.")

            return obj


        except Exception as e:
            print(f"Error while creating {self.model}.")
            print("Rolling back the database commit.")
            print(e)
            db.rollback()




