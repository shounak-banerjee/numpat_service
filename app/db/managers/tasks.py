from app.services.transformer_inference import predict_skills
from app.db.managers.base import BaseManager
from typing import Optional, Any, List, Tuple, Dict, Union
import uuid
class TasksManager(BaseManager):
    async def predict_skills(self, *, dimension: str, skills: List[str], X_test: List[List[str]], models_dict: Dict[str,Any], model_qnli: Any, tokenizer_qnli: Any, tokenizer: Any) -> Dict[str, Any]:
        response = await predict_skills(skills=skills, X_test=X_test, models_dict=models_dict, model_qnli=model_qnli, tokenizer_qnli=tokenizer_qnli,global_tokenizer=tokenizer)
        task = {
            'id': str(uuid.uuid4()),
            'dimension': dimension,
            'skills': skills,
            'X_test': X_test,
            'response': response
        }
        await self.create_one(task)
        return task