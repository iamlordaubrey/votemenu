from pydantic import BaseModel


class BaseVoteSchema(BaseModel):
    employee_id: str
    menu_one_id: str

    class Config:
        orm_mode = True


class RetrieveVoteSchema(BaseVoteSchema):
    id: str
