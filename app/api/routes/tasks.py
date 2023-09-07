from fastapi import APIRouter, Depends, HTTPException, Body
from starlette import status
from app.db.managers import TasksManager, ModelManagerFactory
from app.db.models.tasks import Tasks
from app.core.config import get_app_settings
from app.core.logging import LOG
from app.db.schemas.tasks import TaskInCreateSchema, TaskInResponseSchema

router = APIRouter()

settings = get_app_settings()
settings.configure_logging()

@router.post(
    "/predict",
    status_code=status.HTTP_201_CREATED,
    response_model=TaskInResponseSchema,
    name="tasks:create-task",
)
async def skill_tag(
    task_create: TaskInCreateSchema = Body(...),
    task_manager: TasksManager = Depends(ModelManagerFactory.get_model_manager_callable(model_type=Tasks)),
) -> TaskInResponseSchema:
   
    task: Tasks = await task_manager.predict_skills(
        dimension=task_create.dimension,
        skills=task_create.skills,
        X_test=task_create.X_test,
    )

    LOG.success(f"Task created successfully: {task}")
    # return TaskInResponseSchema.from_orm(task)
    return task