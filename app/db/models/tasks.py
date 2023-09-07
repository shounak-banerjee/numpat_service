from typing import List, Dict
from pydantic import validator
from app.utils.custom_enum import CustomEnum
from app.common.model import BaseModel

class TaskType(CustomEnum):
    LEARNING_AND_DEVELOPMENT = "L&D"

class Tasks(BaseModel):
    dimension: str
    skills: List[str]
    X_test: List[List[str]]
    response: Dict[str, List[int]]

    @validator("dimension", pre=True, always=True)
    def validate_task_type(cls, value: str) -> str:
        if not value or not TaskType.has_value(value=value):
            raise ValueError(f"invalid value provided for the field 'dimension'")
        return value