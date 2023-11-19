from fastapi import APIRouter, Depends, HTTPException, Body
from starlette import status
from app.db.managers import TasksManager, ModelManagerFactory
from app.db.models.tasks import Tasks
from app.core.config import get_app_settings
from app.core.logging import LOG
from app.db.schemas.tasks import TaskInCreateSchema, TaskInResponseSchema
from transformers import LlamaForCausalLM, LlamaTokenizer
import torch

router = APIRouter()

settings = get_app_settings()
settings.configure_logging()

from peft import PeftModel

def load_peft_model(model, peft_model):
    peft_model = PeftModel.from_pretrained(model, peft_model, offload_dir="llama_finetune/offload")
    return peft_model

def load_model(model_name, quantization):
    # model = LlamaForCausalLM.from_pretrained(
    #     model_name,
    #     return_dict=True,
    #     load_in_8bit=True if quantization else None,
    #     device_map="auto" if quantization else None,
    #     # load_in_8bit=quantization,
    #     # device_map="auto",
    #     low_cpu_mem_usage=True,
    #     offload_folder="llama_finetune/offload",
    #     offload_state_dict = True
    # )
    model =LlamaForCausalLM.from_pretrained(model_name, load_in_8bit=True, device_map='auto', torch_dtype=torch.float16)
    # model =LlamaForCausalLM.from_pretrained(model_name, load_in_8bit=False, device_map='auto', torch_dtype=torch.float16)
    # model = LlamaForCausalLM.from_pretrained(
    #         model_name,
    #         load_in_8bit=True if quantization else None,
    #         device_map="auto" if quantization else None,
    #     )
    return model

model_id="/mnt/llama_finetune/model"
model_peft="/mnt/llama_finetune/Leadership_and_Responsibility"
model_id_tok="/mnt/llama_finetune/model"
llama_tokenizer = LlamaTokenizer.from_pretrained(model_id_tok)
# model =LlamaForCausalLM.from_pretrained(model_id, load_in_8bit=True, device_map='auto', torch_dtype=torch.float16)
quantization=False
model = load_model(model_id, quantization)
llama_model = load_peft_model(model, model_peft)

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
        llama_model=llama_model,
        llama_tokenizer=llama_tokenizer
    )

    LOG.success(f"Task created successfully: {task}")
    # return TaskInResponseSchema.from_orm(task)
    return task