"""
Schemas pydantic
"""

from pydantic import BaseModel, root_validator

from api.utils.custom_http_response import CustomHTTPException


class POSTRequest(BaseModel):
    """
    Schema validator to payload
    """

    init_date: str = None
    end_date: str = None
