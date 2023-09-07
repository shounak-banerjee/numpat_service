from typing import List, Optional,Dict,DefaultDict,Any
from sqlalchemy import JSON
from app.common.schema import RWSchema, DateTimeModelMixin, IDModelMixin
from fastapi import Request

class TaskSchema(RWSchema):
    dimension: str
    skills: List[str]
    X_test: List[List[str]]
    
class TaskInDBSchema(TaskSchema, DateTimeModelMixin, IDModelMixin):
    # user: Users
    pass

class TaskInCreateSchema(RWSchema):
    dimension: str
    skills: List[str]
    X_test: List[List[str]]


class TaskInResponseSchema(RWSchema, IDModelMixin, DateTimeModelMixin):
    response: Dict[str,List[int]]
