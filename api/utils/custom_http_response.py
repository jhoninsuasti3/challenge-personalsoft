"""
Custom response api
"""

from ast import literal_eval

from fastapi import Request
from fastapi.exceptions import HTTPException, RequestValidationError
from fastapi.responses import JSONResponse


class CustomHTTPException(HTTPException):
    """
    CustomHTTPException class extends the base HTTPException class to provide
        a custom exception
    with additional data and features.

    Args:
        status_code (int): The HTTP status code associated with the exception.
        data (str): A string describing the type or category of the error.
        message (str): A human-readable error message providing more context.
        requests (dict, optional): A dictionary containing request-related
            data. Defaults to None.

    Attributes:
        detail (dict): A dictionary containing detailed information about the
            exception.


    """

    def __init__(
        self,
        status_code: int,
        data: str,
        message: str,
        internal_message: str = None,
        requests: dict = None,
    ):
        super().__init__(status_code)
        self.detail = {"status": "error", "data": data, "message": message}

        cloudwatch_log = self.detail
        if internal_message:
            cloudwatch_log["message"] += " - " + internal_message
        if requests:
            cloudwatch_log["requests"] = requests


async def http_exception_handler(request: Request, exc: CustomHTTPException):
    """
    Handle custom HTTP exceptions by generating a JSON response containing
        error details.

    Args:
        request (Request): The incoming HTTP request causing the exception.
        exc (CustomHTTPException): The custom exception to be handled.

    Returns:
        JSONResponse: A JSON response containing error details from the
            provided exception.
    """
    return JSONResponse(status_code=exc.status_code, content=exc.detail)


async def validation_exception_handler(
    request: Request, exc: RequestValidationError
):
    """
    Handle validation errors by generating a JSON response containing error
        details.

    This function is designed to handle exceptions of type
        `RequestValidationError` raised during
    request validation processes.

    Args:
        request (Request): The incoming HTTP request triggering the validation
            error.
        exc (RequestValidationError): The validation exception to be handled.

    Returns:
        JSONResponse: A JSON response containing error details for the
            validation exception.
    """
    error_messages = []
    for error in exc.errors():
        error_messages.append(
            {
                "loc": error.get("loc", []),
                "msg": error.get("msg"),
                "type": error.get("type"),
                "ctx": error.get("ctx", {}),
            }
        )

    return JSONResponse(
        status_code=422,
        content={
            "status": "error",
            "data": error_messages,
            "message": "Error de validación de request.",
        },
    )
