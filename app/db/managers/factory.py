from typing import Dict, Type
from app.db.models.tasks import Tasks
from app.db.managers.tasks import TasksManager
from app.db.managers.base import BaseManager
from app.common.model import BaseModel
from typing import Dict, Type, Callable


class ModelManagerFactory:
    MANAGERS: Dict[Type[BaseModel], Type[BaseManager]] = {}

    @classmethod
    def add_model_manager(cls, model: Type[BaseModel], manager: Type[BaseManager]) -> None:
        cls.MANAGERS[model] = manager(table_name=model.__name__)

    @classmethod
    def get_model_manager(cls, model_type: Type[BaseModel]) -> BaseManager:
        return cls.MANAGERS.get(model_type)

    @classmethod
    def get_model_manager_callable(cls, model_type: Type[BaseModel]) -> Callable[[], BaseManager]:
        """Class method that returns a callable that returns model manager instance of model_type provided"""
        def _get_model_manager_callable() -> BaseManager:
            return ModelManagerFactory.MANAGERS.get(model_type)
        return _get_model_manager_callable

# Registering the manager
ModelManagerFactory.add_model_manager(Tasks, TasksManager)