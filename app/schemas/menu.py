from pydantic import BaseModel


class BaseMenuSchema(BaseModel):
    content: dict[str, str | dict]
    restaurant_id: str

    class Config:
        orm_mode = True


class RetrieveMenuSchema(BaseMenuSchema):
    id: str
