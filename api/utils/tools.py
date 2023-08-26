"""
Generic funcions to ms
"""
from sqlalchemy.orm import Session
from datetime import datetime


def generic_post(data, db: Session):
    db.add(data)
    db.commit()
    db.refresh(data)
    return data


def format_date(date: str) -> str:
    try:
        date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        raise ValueError("Invalid date format. Use 'YYYY-MM-DD HH:MM:SS'.")
    return date


def update_generic(generic_model, id, data, db: Session):
    db.query(generic_model).filter(generic_model.id == id).update(data)
    db.commit()
    return id
