from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class CustomerBase(BaseModel):
    first_name: str = Field(..., example="John")
    address: str = Field(..., example="Jl. Raya Kebayoran Lama No. 12")
    last_name: str = Field(..., example="Doe")


class CustomerCreate(CustomerBase):
    start_date: str = Field(..., example="2021-01-01")
    end_date: str = Field(..., example="2021-12-31")


class CustomersResults(CustomerBase):
    id: str
    start_date: Optional[datetime]
    end_date: Optional[datetime]

    class Config:
        orm_mode = True


class CustomerModel(BaseModel):
    id: str
    first_name: str = Field(..., example="John")
    address: str = Field(..., example="Jl. Raya Kebayoran Lama No. 12")
    last_name: str = Field(..., example="Doe")
    is_active: bool = Field(..., example=True)
    start_date: Optional[datetime]
    end_date: Optional[datetime]
