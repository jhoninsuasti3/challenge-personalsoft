from sqlalchemy.orm import Session
from api.database import models


def get_active_customers(db: Session):
    customers = db.query(models.Customers).filter(models.Customers.is_active == True).all()
    return customers
