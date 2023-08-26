from fastapi import APIRouter, HTTPException, status, Depends
from api.repository import customers as customer_repository
from api.database import models
from sqlalchemy.orm import Session
from api.database.db import get_db
from api.utils.tools import generic_post
from api.schemas import customer as schema_customer
from fastapi_pagination import Page, Params, paginate

router = APIRouter(prefix="/customers", tags=["customers"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schema_customer.CustomersResults)
def create_customer(customer: schema_customer.CustomerBase, db: Session = Depends(get_db)):
    try:
        customer = models.Customers(**customer.dict())
        customer = generic_post(customer, db)
        return customer
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/active", status_code=status.HTTP_200_OK, response_model=Page[schema_customer.CustomersResults])
def get_active_customers(db: Session = Depends(get_db), params: Params = Depends()):
    try:
        customers = customer_repository.get_active_customers(db)
        return paginate(customers, params)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/{customer_id}/orders", status_code=status.HTTP_200_OK)
def get_customers(customer_id: str, db: Session = Depends(get_db), params: Params = Depends()):
    try:
        customer_repository.get_customer(customer_id, db)
        customers = customer_repository.get_orders_by_customer(customer_id, db)
        return paginate(customers, params)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
