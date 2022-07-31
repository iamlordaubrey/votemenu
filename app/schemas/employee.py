from pydantic import BaseModel


class BaseEmployeeSchema(BaseModel):
    first_name: str
    last_name: str
    restaurant_id: str

    class Config:
        orm_mode = True


class RetrieveEmployeeSchema(BaseEmployeeSchema):
    id: str
