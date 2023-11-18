import gc
import torch
from datasets import Dataset
from datasets.dataset_dict import DatasetDict
from torch.utils.data import DataLoader
import torch
import torch.nn as nn
from transformers import AdamW,get_scheduler,AutoTokenizer,AutoModel,AutoConfig,DataCollatorWithPadding,BertTokenizer, BertForSequenceClassification
import json
import boto3
import io

tokenizer = AutoTokenizer.from_pretrained('sentence-transformers/paraphrase-mpnet-base-v2')
tokenizer.model_max_len=512

def load_model_from_s3(bucket_name, model_key,device):
    s3 = boto3.client('s3',region_name='ap-south-1')
    obj = s3.get_object(Bucket=bucket_name, Key=model_key)
    model_bytes = obj['Body'].read()
   
    # Load the model directly from bytes
    model = torch.load(io.BytesIO(model_bytes),map_location=device)
    model.eval()  # Set the model to evaluation mode if it's a neural network
    return model

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

def qnli_inference(question, passage):
    model_name_qnli = "gchhablani/bert-base-cased-finetuned-qnli"  # You can replace this with a model fine-tuned on QNLI if you have one.
    tokenizer_qnli = BertTokenizer.from_pretrained(model_name_qnli)
    model_qnli = BertForSequenceClassification.from_pretrained(model_name_qnli)  # Replace with a fine-tuned model if available
    inputs = tokenizer_qnli(question, passage, return_tensors="pt", truncation=True, padding=True, max_length=512)
    model_qnli.eval()
    with torch.no_grad():
        outputs = model_qnli(**inputs)
        print(outputs)
        logits = outputs.logits
        probabilities = torch.nn.functional.softmax(logits, dim=1)
        print(probabilities[0])
        pred_label = torch.argmax(probabilities, dim=1).item()
    if((probabilities[0][1])>0.95):
      return False
    else:
      return True

def trained_embeddings_predictions(tokenized_data,data_collator,skill):
    print(skill)
    device=torch.device('cpu')
    try:
        try:
            print("Sagemaker inference")
            model=torch.load('ml/model/'+skill+'.pt',map_location=device)
        except:
            print("s3_inference")
            model = load_model_from_s3('numpat-models', skill+'.pt',device)
    except:
        raise Exception("Could not load model from local or s3.")
        
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
    relevancy_array=[]
    for question_answer_pair in X_test:
        if(qnli_inference(question_answer_pair[0], question_answer_pair[1])):
            relevancy_array.append(1)
        else:
            relevancy_array.append(0)
            
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
        for _ in range(len(predictions[skill])):
            predictions[skill][_]*=relevancy_array[_]
    return predictions