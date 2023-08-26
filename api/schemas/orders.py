from pydantic import BaseModel, Field, root_validator
from datetime import timedelta
from typing import Optional
from api.database.models import WorkOrderStatusEnum
from api.utils.tools import format_date
from api.schemas.customer import CustomerModel
from fastapi import HTTPException
import enum


class WorkBase(BaseModel):
    customer_id: str = Field(..., example="123e4567-e89b-12d3-a456-426614174000")
    title: str = Field(..., example="Title example")
    planned_date_begin: str = Field(..., example="2021-01-01 00:00:00")
    planned_date_end: str = Field(..., example="2021-12-31 23:59:59")
    status: WorkOrderStatusEnum

    @root_validator
    def validate_planned_date_end(cls, values: dict) -> dict:
        format_date(values.get("planned_date_end"))
        return values

    @root_validator
    def validate_planned_date_begin(cls, values: dict) -> dict:
        format_date(values.get("planned_date_begin"))
        return values

    @root_validator
    def validate_diif_dates(cls, values: dict) -> dict:
        planned_date = format_date(values.get("planned_date_begin"))
        planned_date_end = format_date(values.get("planned_date_end"))
        max_time_difference = timedelta(hours=2)

        if (planned_date_end - planned_date) > max_time_difference:
            raise ValueError("El tiempo máximo de ejecución es de 2 horas.")
        return values


class WorkOrderModel(BaseModel):
    id: str
    title: str


class OrderAndCustomerModel(BaseModel):
    work_order: WorkOrderModel
    customer: CustomerModel


class OrderFilter(BaseModel):
    since: Optional[str]
    until: Optional[str]
    status: Optional[WorkOrderStatusEnum]

    @root_validator
    def validate_data(cls, values: dict) -> dict:
        since = values.get("since")
        until = values.get("until")

        if since and not until:
            raise HTTPException(
                status_code=404, detail="Si se proporciona 'since', 'until' también debe proporcionarse"
            )
        elif until and not since:
            raise HTTPException(
                status_code=404, detail="Si se proporciona 'until', 'since' también debe proporcionarse"
            )
        elif since and until:
            try:
                since = format_date(since)
                until = format_date(until)
                if since > until:
                    raise HTTPException(status_code=404, detail="'since' no puede ser mayor a 'until'")
            except Exception as e:
                raise HTTPException(status_code=404, detail=str(e.detail))
        return values


class WorkOrderUpdate(enum.Enum):
    DONE = "DONE"
    CANCELLED = "CANCELLED"


class OrderUpdate(BaseModel):
    status: Optional[WorkOrderUpdate]


class WorkResponse(BaseModel):
    id: str
    customer_id: str
    title: str

    class Config:
        orm_mode = True
