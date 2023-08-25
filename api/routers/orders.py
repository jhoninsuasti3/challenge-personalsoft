from fastapi import APIRouter, HTTPException, status


router = APIRouter(prefix="/orders", tags=["orders"])


@router.post("/", status_code=status.HTTP_200_OK)
def create_orders():
    pass
