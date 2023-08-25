from pydantic import BaseModel, Field, validator, root_validator
from datetime import datetime
from typing import Optional
from api.database.models import WorkOrderStatusEnum


class WorkBase(BaseModel):
    customer_id: str = Field(..., example="123e4567-e89b-12d3-a456-426614174000")
    title: str = Field(..., example="Title example")
    planned_date_begin: str = Field(..., example="2021-01-01")
    planned_date_end: str = Field(..., example="2021-12-31")
    status: WorkOrderStatusEnum

    # @validator("planned_date_begin")
    # def validate_planned_date_begin(cls, value):
    #     try:
    #         datetime.strptime(value, "%Y-%m-%d")
    #         return value
    #     except ValueError:
    #         raise ValueError("Invalid date format. Use 'YYYY-MM-DD'.")

    # @validator("planned_date_end")
    # def validate_planned_date_end(cls, value):
    #     try:
    #         datetime.strptime(value, "%Y-%m-%d")
    #         return value
    #     except ValueError:
    #         raise ValueError("Invalid date format. Use 'YYYY-MM-DD'.")

    @root_validator
    def validate_fields(cls, values: dict) -> dict:
        pass
