from pydantic import BaseModel


class BaseVoteSchema(BaseModel):
    employee_id: str
    menu_one_id: str

    class Config:
        orm_mode = True


class RetrieveVoteSchema(BaseVoteSchema):
    id: str


class BaseVoteSchemaV2(BaseVoteSchema):
    menu_two_id: str
    menu_three_id: str


class RetrieveVoteSchemaV2(BaseVoteSchemaV2):
    id: str
