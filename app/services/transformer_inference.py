import gc
import torch
from datasets import Dataset
from datasets.dataset_dict import DatasetDict
from torch.utils.data import DataLoader
import torch
import torch.nn as nn
from transformers import AdamW,get_scheduler,AutoTokenizer,AutoModel,AutoConfig,DataCollatorWithPadding
import json

tokenizer = AutoTokenizer.from_pretrained('sentence-transformers/paraphrase-mpnet-base-v2')
tokenizer.model_max_len=512

def preprocess_function(examples):
    return tokenizer(examples["text1"],examples["text2"], truncation=True)
def preprocess_function_answer_only(examples):
    return tokenizer(examples["text1"], truncation=True)

# define mean pooling function
def mean_pool(token_embeds, attention_mask):
    # reshape attention_mask to cover 768-dimension embeddings
    in_mask = attention_mask.unsqueeze(-1).expand(
        token_embeds.size()
    ).float()
    # perform mean-pooling but exclude padding tokens (specified by in_mask)
    pool = torch.sum(token_embeds * in_mask, 1) / torch.clamp(
        in_mask.sum(1), min=1e-9
    )
    return pool

def trained_embeddings_predictions(tokenized_data,data_collator,skill):
    device=torch.device('cpu')
    print(skill)
    model=torch.load('/mnt/transformers_backend/transformers_backend/trained_embeddings_inference/models/latest_models/'+skill+'.pt',map_location=device)
    test_dataloader = DataLoader(
        tokenized_data["test"], batch_size=1, collate_fn=data_collator
    )
    conf=[]
    p=[]
    for batch in test_dataloader:
        batch = {k: v.to(device) for k, v in batch.items()}
        # print("batch",batch)
        with torch.no_grad():
            outputs = model(**batch)
        # l=[]
        logits = outputs.logits
        m = nn.Softmax(dim=1)
        input = logits
        out = m(input)
        conf.append(out)
        # print(out[0])
        predictions = torch.argmax(logits, dim=-1)
        # conf.append(out)
        p.append(predictions)
    p = [x.cpu().numpy().item() for xs in p for x in xs]
    flat_list = [list(x.cpu().numpy()) for xs in conf for x in xs]
    return p

async def predict_skills(skills,X_test):
    predictions={}
    # d = {'test':Dataset.from_dict({'text1':[ex[0] for ex in X_test],'text2':[ex[1] for ex in X_test]})}
    # d =DatasetDict(d)
    # tokenized_data = d.map(preprocess_function, batched=True)
    # tokenized_data.set_format("torch",columns=["input_ids", "attention_mask"])
    # data_collator = DataCollatorWithPadding(tokenizer=tokenizer)
#     eval_dataloader = DataLoader(
#     tokenized_data["test"], batch_size=30, collate_fn=data_collator
# )
    for skill in skills:
        if(skill in ["Communication","Collaboration"]):
            print("INSIDE ANSWER ONLY")
            d = {'test':Dataset.from_dict({'text1':[ex[1] for ex in X_test]})}
            d =DatasetDict(d)
            tokenized_data = d.map(preprocess_function_answer_only, batched=True)
            tokenized_data.set_format("torch",columns=["input_ids", "attention_mask"])
            data_collator = DataCollatorWithPadding(tokenizer=tokenizer)
        else:
            d = {'test':Dataset.from_dict({'text1':[ex[0] for ex in X_test],'text2':[ex[1] for ex in X_test]})}
            d =DatasetDict(d)
            tokenized_data = d.map(preprocess_function, batched=True)
            tokenized_data.set_format("torch",columns=["input_ids", "attention_mask"])
            data_collator = DataCollatorWithPadding(tokenizer=tokenizer)
            
        predictions[skill]=trained_embeddings_predictions(tokenized_data,data_collator,skill)
    
    return predictions