from sqlalchemy import Column, String, DateTime, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid
from sqlalchemy import ForeignKey
from sqlalchemy import Enum
from api.database.database import Base
import enum


def generate_uuid():
    return str(uuid.uuid4())


class WorkOrderStatusEnum(enum.Enum):
    NEW = "NEW"
    DONE = "DONE"
    CANCELLED = "CANCELLED"


class Customers(Base):
    __tablename__ = "customers"
    id = Column(String, primary_key=True, default=generate_uuid, unique=True)
    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)
    address = Column(String(255), nullable=False)
    start_date = Column(DateTime(timezone=True), nullable=True)
    end_date = Column(DateTime(timezone=True), nullable=True)
    is_active = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())


class WorkOrders(Base):
    __tablename__ = "work_orders"
    id = Column(String, primary_key=True, default=generate_uuid, unique=True)
    customer_id = Column(String, ForeignKey("customers.id"))
    title = Column(String(255), nullable=False)
    planned_date_begin = Column(DateTime(timezone=True))
    planned_date_end = Column(DateTime(timezone=True))
    status = Column(Enum(WorkOrderStatusEnum), default=WorkOrderStatusEnum.NEW)
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())
