from sqlalchemy.orm import Session
from api.database import models
from fastapi import HTTPException


def get_active_customers(db: Session):
    customers = db.query(models.Customers).filter(models.Customers.is_active == True).all()
    return customers


def get_customer(id_customer: str, db: Session):
    customer = db.query(models.Customers).filter(models.Customers.id == id_customer).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer


def get_orders_customer(id_customer: int, db: Session):
    orders = db.query(models.Customers).filter(models.Customers.id == id_customer).all()
    return orders


def get_orders_by_customer(id_customer: str, db: Session):
    orders = (
        db.query(models.WorkOrders)
        .select_from(models.Customers)
        .join(models.WorkOrders, models.WorkOrders.customer_id == models.Customers.id)
        .filter(models.Customers.id == id_customer)
        .all()
    )
    return orders
