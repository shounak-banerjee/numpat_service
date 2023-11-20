from fastapi import APIRouter, Depends, HTTPException, Body
from starlette import status
from app.db.managers import TasksManager, ModelManagerFactory
from app.db.models.tasks import Tasks
from app.core.config import get_app_settings
from app.core.logging import LOG
from app.db.schemas.tasks import TaskInCreateSchema, TaskInResponseSchema
import torch
from transformers import AutoTokenizer, BertTokenizer, BertForSequenceClassification

router = APIRouter()

settings = get_app_settings()
settings.configure_logging()

device=torch.device("cuda" if torch.cuda.is_available() else "cpu")
models_dict={}
skills=["Problem solving and Critical Thinking","Communication","Collaboration","Creativity and Innovation"]
for skill in skills:
    try:
        print("Sagemaker inference")
        models_dict[skill]=torch.load('ml/model/'+skill+'.pt',map_location=device)
    except:
        raise Exception("Could not load model from local or s3.")


tokenizer = AutoTokenizer.from_pretrained('sentence-transformers/paraphrase-mpnet-base-v2')
tokenizer.model_max_len=512
model_name_qnli = "gchhablani/bert-base-cased-finetuned-qnli"  # You can replace this with a model fine-tuned on QNLI if you have one.
tokenizer_qnli = BertTokenizer.from_pretrained(model_name_qnli)
model_qnli = BertForSequenceClassification.from_pretrained(model_name_qnli)  # Replace with a fine-tuned model if available

@router.get('/ping')
async def ping():
    return {"message": "ok"}
@router.post(
    "/invocations",
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
        models_dict=models_dict,
        model_qnli=model_qnli,
        tokenizer_qnli=tokenizer_qnli,
        tokenizer=tokenizer
    )

    LOG.success(f"Task created successfully: {task}")
    # return TaskInResponseSchema.from_orm(task)
    return task