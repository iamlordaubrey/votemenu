from pydantic import BaseModel


class BaseRestaurantSchema(BaseModel):
    name: str
    location: str

    class Config:
        orm_mode = True


class RetrieveRestaurantSchema(BaseRestaurantSchema):
    id: str
