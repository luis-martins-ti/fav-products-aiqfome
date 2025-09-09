from pydantic import BaseModel
from typing import List
from app.schemas.product import ProductOut


class FavoriteCreate(BaseModel):
    external_id: int


class FavoriteOut(BaseModel):
    id: int
    product: ProductOut

    class Config:
        orm_mode = True
