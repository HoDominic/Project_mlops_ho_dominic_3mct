from fastapi import FastAPI
from schemas.patient import Patient as PatientSchema
from uuid import uuid4
from schemas.patient import Patient
import database as db




from routers import (
    patient_router as patient # Just to make an alias, because it looks nicer.
    
)


# #start db
db.start_db()


app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Let's detect diabetes!"}


# poetry run uvicorn main:app --reload


app.include_router(patient.router)

