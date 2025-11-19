from typing import List
from fastapi import APIRouter, Depends, Body, status
from sqlalchemy.orm import Session
import uuid

from app.core.dependencies import get_db, get_current_active_user
from .failure_analysis_schemas import (
    RCAItemCreate, RCAItemUpdate, 
    FailureSymptomRead, FailureModeRead, FailureCauseRead
)
from .failure_analysis_crud import crud_symptom, crud_mode, crud_cause

router = APIRouter()

# --- 1. SINTOMAS (Symptoms) ---

@router.get("/failure-symptoms", response_model=List[FailureSymptomRead])
def read_symptoms(db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    return crud_symptom.get_multi(db, skip=skip, limit=limit)

@router.post("/failure-symptoms", response_model=FailureSymptomRead, status_code=status.HTTP_201_CREATED)
def create_symptom(obj_in: RCAItemCreate, db: Session = Depends(get_db)):
    return crud_symptom.create(db, obj_in=obj_in)

@router.put("/failure-symptoms/{id}", response_model=FailureSymptomRead)
def update_symptom(id: uuid.UUID, obj_in: RCAItemUpdate, db: Session = Depends(get_db)):
    db_obj = crud_symptom.get(db, id)
    if not db_obj: return None # Ou raise 404
    return crud_symptom.update(db, db_obj=db_obj, obj_in=obj_in)

@router.delete("/failure-symptoms/{id}", response_model=FailureSymptomRead)
def delete_symptom(id: uuid.UUID, db: Session = Depends(get_db)):
    return crud_symptom.remove(db, id=id)


# --- 2. MODOS DE FALHA (Modes) ---

@router.get("/failure-modes", response_model=List[FailureModeRead])
def read_modes(db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    return crud_mode.get_multi(db, skip=skip, limit=limit)

@router.post("/failure-modes", response_model=FailureModeRead, status_code=status.HTTP_201_CREATED)
def create_mode(obj_in: RCAItemCreate, db: Session = Depends(get_db)):
    return crud_mode.create(db, obj_in=obj_in)

@router.put("/failure-modes/{id}", response_model=FailureModeRead)
def update_mode(id: uuid.UUID, obj_in: RCAItemUpdate, db: Session = Depends(get_db)):
    db_obj = crud_mode.get(db, id)
    if not db_obj: return None
    return crud_mode.update(db, db_obj=db_obj, obj_in=obj_in)

@router.delete("/failure-modes/{id}", response_model=FailureModeRead)
def delete_mode(id: uuid.UUID, db: Session = Depends(get_db)):
    return crud_mode.remove(db, id=id)


# --- 3. CAUSAS DE FALHA (Causes) ---

@router.get("/failure-causes", response_model=List[FailureCauseRead])
def read_causes(db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    return crud_cause.get_multi(db, skip=skip, limit=limit)

@router.post("/failure-causes", response_model=FailureCauseRead, status_code=status.HTTP_201_CREATED)
def create_cause(obj_in: RCAItemCreate, db: Session = Depends(get_db)):
    return crud_cause.create(db, obj_in=obj_in)

@router.put("/failure-causes/{id}", response_model=FailureCauseRead)
def update_cause(id: uuid.UUID, obj_in: RCAItemUpdate, db: Session = Depends(get_db)):
    db_obj = crud_cause.get(db, id)
    if not db_obj: return None
    return crud_cause.update(db, db_obj=db_obj, obj_in=obj_in)

@router.delete("/failure-causes/{id}", response_model=FailureCauseRead)
def delete_cause(id: uuid.UUID, db: Session = Depends(get_db)):
    return crud_cause.remove(db, id=id)