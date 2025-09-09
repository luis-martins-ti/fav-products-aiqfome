from pydantic import BaseModel


class ProductOut(BaseModel):
    id: int
    external_id: int
    title: str
    image: str
    price: float
    rating_rate: float
    rating_count: int

    class Config:
        orm_mode = True
