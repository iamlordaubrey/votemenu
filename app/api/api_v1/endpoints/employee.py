from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.auth.jwt import get_current_user
from app.database import get_db
from app.models import User
from app.schemas.employee import RetrieveEmployeeSchema, BaseEmployeeSchema
from app.services.crud_db import create_new_employee

router = APIRouter()


@router.post('', status_code=201, response_model=RetrieveEmployeeSchema, summary='Creates an employee')
async def create_employee(
        employee: BaseEmployeeSchema, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    employee = create_new_employee(db=db, employee=employee)
    return jsonable_encoder(employee)
