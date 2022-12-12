from fastapi import FastAPI,HTTPException
import json 
#app = FastAPI()
from schemas.patient import Patient
from fastapi import APIRouter
from database import db
from models.patient_model import Patient as PatientRepo




#APIROUTER
router = APIRouter(prefix="/patient",
tags=["Patient"],
responses={404: {"Patient": "Not found"}},
)


#OPLETTEN /patient door APIrouter!

#GET
@router.get("/all")
async def get_all():
    patients = db.patients.find()
    return patients

#POST
@router.post("/add_one")
async def create(patient: Patient):
    patient = patient.dict()
    db.patients.insert_one(patient)
    return patient

#GET  PATIENT BY ID
@router.get("{id}")
async def get_by_id(id: str):
    patient = db.patients.find_one({"_id": id})
    if patient:
        return patient
    raise HTTPException(status_code=404, detail="Patient not found")



#Repo
repo = PatientRepo()

@router.get("/get_all_from_repo")
async def get_all_patients():
    objects = repo.get_all()
    if objects is None:
        raise HTTPException(status_code=400, detail="Something went wrong here!")
    return objects

@router.get("/get_by_id_from_repo/{id}")
async def get_patient_by_id(id: str):
    object = repo.get_by(id=id)
    if object is None:
        raise HTTPException(status_code=400, detail="Something went wrong here!")
    return object



@router.post("/add_from_repo")
def  post_patient(patient: Patient):
    created_object = repo.create(patient)
    if created_object is None:
        raise HTTPException(status_code=400, detail=f"A bird like that already exists.")
    return created_object




