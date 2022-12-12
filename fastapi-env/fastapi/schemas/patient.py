# patient.py
from typing import Optional
from pydantic import BaseModel


class Patient(BaseModel):
   # uuid: Optional[str]
    id: str
    name: str
    pregnancies: int
    glucose: int
    bloodpressure: int
    skinthickness: int
    insulin: int
    bmi: float
    dpf: float
    age: int



    class Config:
            orm_mode = True


    def sayHello(self):
            print("Hello, I am " + self.name)

  