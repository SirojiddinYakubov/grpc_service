from typing import Optional

from pydantic import BaseModel


class CreateCourseTopic(BaseModel):
    name: str
    description: Optional[str]
    parent_id: Optional[str]
    locale_id: int
