from app.services.transformer_inference import predict_skills
from app.db.managers.base import BaseManager
from typing import Optional, Any, List, Tuple, Dict, Union
import uuid
class TasksManager(BaseManager):
    async def predict_skills(self, *, dimension: str, skills: List[str], X_test: List[List[str]],llama_model:Any, llama_tokenizer: Any) -> Dict[str, Any]:
        response = await predict_skills(skills=skills, X_test=X_test, llama_model=llama_model, llama_tokenizer=llama_tokenizer)
        task = {
            'id': str(uuid.uuid4()),
            'dimension': dimension,
            'skills': skills,
            'X_test': X_test,
            'response': response
        }
        try:
            await self.create_one(task)
        except:
            pass
        return task