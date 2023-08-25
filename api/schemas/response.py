"""
Response api create customer schemas
"""

from typing import Optional

from pydantic import BaseModel


class POSTResponse(BaseModel):
    """
    Response api create customer schema
    """

    status: str
    data: Optional[dict]
