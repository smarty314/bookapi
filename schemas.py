# python/cloudopsportal/src/cloudops/portal/schemas.py
from pydantic import BaseModel
from typing import Optional

class APIResponse(BaseModel):
    books: Optional[list]
    search: Optional[str]
    count: int
    status_code: Optional[str]