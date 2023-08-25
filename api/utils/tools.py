"""
Generic funcions to ms
"""
from sqlalchemy.orm import Session


def generic_post(data, db: Session):
    db.add(data)
    db.commit()
    db.refresh(data)
    return data
