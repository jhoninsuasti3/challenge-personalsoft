from fastapi import APIRouter, HTTPException, status, Depends
from api.repository import orders as repository_order
from api.repository import customers as repository_customer
from api.schemas.orders import WorkBase
from sqlalchemy.orm import Session
from api.database.db import get_db
from datetime import datetime
from api.database import models
from api.utils.tools import generic_post, update_generic
from api.utils.utils import format_data_response
from api.schemas.orders import OrderAndCustomerModel, OrderFilter, OrderUpdate
from fastapi_pagination import Params, paginate
from api.tasks import add_event

router = APIRouter(prefix="/orders", tags=["orders"])


@router.post("/", status_code=status.HTTP_200_OK)
def create_orders(order_req: WorkBase, db: Session = Depends(get_db)):
    try:
        order_req = order_req.dict(exclude_unset=True)
        order = repository_order.validate_exist(order_req.get("customer_id"), db)
        if order:
            data = {"start_date": datetime.now(), "is_active": True}
            update_generic(models.Customers, order_req.get("customer_id"), data, db)
        order_db = models.WorkOrders(**order_req)
        generic_post(order_db, db)
    except HTTPException as e:
        raise e
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )
    return {"message": "Order created successfully!"}


@router.get("/{order_id}", status_code=status.HTTP_200_OK, response_model=OrderAndCustomerModel)
def get_order_by_id(order_id: str, db: Session = Depends(get_db)):
    try:
        order_data, customer_data = repository_order.get_order_by_id(order_id, db)
        response = format_data_response(order_data, customer_data)
    except HTTPException as e:
        raise e
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )
    return response


@router.get("/", status_code=status.HTTP_200_OK)
def filter_orders(data: OrderFilter = Depends(), db: Session = Depends(get_db), params: Params = Depends()):
    try:
        data_filter = data.dict(exclude_unset=True)
        order_data_filter = repository_order.get_orders_filter(data_filter, db)
    except HTTPException as e:
        raise e
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )
    return paginate(order_data_filter, params)


@router.patch("/{order_id}", status_code=status.HTTP_200_OK)
def update_order(order_id: str, data: OrderUpdate, db: Session = Depends(get_db)):
    try:
        data_update = data.dict(exclude_unset=True)
        order = repository_order.get_only_order(order_id, db)
        if order.status.value != "NEW":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Orden no se puede actualizar porque ya fue procesada",
            )
        data_update["status"] = data_update["status"].value
        update_generic(models.WorkOrders, order_id, data_update, db)
        data_response = {
            "status": "success",
            "code": 200,
            "data": data_update,
            "message": f"Update success order {order_id}",
        }
        add_event.delay(
            data_response,
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )
    return {"message": "Order updated successfully!"}
