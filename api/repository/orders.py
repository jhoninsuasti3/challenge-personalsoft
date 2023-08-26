from sqlalchemy.orm import Session
from api.database import models
from fastapi import HTTPException


def validate_exist(customer_id: int, db: Session):
    customer = db.query(models.Customers).filter(models.Customers.id == customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    # validate if customer has orders
    orders = db.query(models.WorkOrders).filter(models.WorkOrders.customer_id == customer_id).first()
    if not orders:
        return True
    return False


def get_only_order(order_id: int, db: Session):
    order = db.query(models.WorkOrders).filter(models.WorkOrders.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


def get_order_by_id(order_id: str, db: Session):
    order = (
        db.query(models.WorkOrders, models.Customers)
        .join(models.Customers, models.Customers.id == models.WorkOrders.customer_id)
        .filter(models.WorkOrders.id == order_id)
        .first()
    )
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    order_data, customer_data = order
    return order_data, customer_data


def get_orders_filter(data_filter: dict, db: Session):
    query = db.query(models.WorkOrders)

    if data_filter.get("since") and data_filter.get("until"):
        query = query.filter(models.WorkOrders.planned_date_begin >= data_filter.get("since")).filter(
            models.WorkOrders.planned_date_end <= data_filter.get("until")
        )

    if data_filter.get("status"):
        query = query.filter(models.WorkOrders.status == data_filter.get("status"))

    orders = query.all()
    return orders
