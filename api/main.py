"""
APP FastAPI
"""


from fastapi import FastAPI
from api.schemas.request import POSTRequest
from api.utils.custom_http_response import (
    CustomHTTPException,
    http_exception_handler,
)
from api.routers import customers
from api.routers import orders

app = FastAPI(title="API enerbit", description="Enerbit API")

app.add_exception_handler(CustomHTTPException, http_exception_handler)


@app.get("/")
async def home():
    """
    Handler for the home route ("/") that returns a simple greeting message.

    Returns:
        str: A plain text message indicating the purpose of the application.
    """
    return "enerbit APIs"


app.include_router(customers.router)
app.include_router(orders.router)
