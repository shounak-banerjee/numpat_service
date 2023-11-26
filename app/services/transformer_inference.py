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

global tokenizer

def load_model_from_s3(bucket_name, model_key,device):
    s3 = boto3.client('s3',region_name='ap-south-1')
    obj = s3.get_object(Bucket=bucket_name, Key=model_key)
    model_bytes = obj['Body'].read()
   
    # Load the model directly from bytes
    model = torch.load(io.BytesIO(model_bytes),map_location=device)
    model.eval()  # Set the model to evaluation mode if it's a neural network
    return model

def preprocess_function(examples, tokenizer):
    return tokenizer(examples["text1"],examples["text2"], truncation=True)
def preprocess_function_answer_only(examples, tokenizer):
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

def qnli_inference(question, passage,model_qnli,tokenizer_qnli):
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

def get_preprocessed_data(model,tokenizer, dataset, skill):
    # dataset = datasets.load_dataset("samsum", split=split)

    prompt = (
        f"Given the question and it's answer, determine if the {skill} skill is present in the answer. :\n Question: {{question}} \nAnswer:{{answer}} \---{skill}:"
    )

    print(prompt)

    def apply_prompt_template(sample):
        return {
            "text": prompt.format(
                question=sample["question"],
                answer=sample["answer"],
                skill=skill,
                eos_token=tokenizer.eos_token,
            )
        }

    dataset = dataset.map(apply_prompt_template, remove_columns=list(dataset.features))
    # print("ddd",dataset["text"])
    answers=[]
    for x,prompt in enumerate(dataset["text"]):
        model_input=tokenizer(prompt, return_tensors="pt").to("cuda")
        model.eval()
        with torch.no_grad():
            model_generation=model.generate(**model_input, max_new_tokens=100)[0]
            answers.append(tokenizer.decode(model_generation, skip_special_tokens=True))
    pred=[]
    for _,answer in enumerate(answers):
        if ("not present" in answer.lower()) or ("no" in answer.lower()) or ("0" in answer.lower()):
            pred.append(0)
        else:
            pred.append(1)
    return pred

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
    device=torch.device("cuda" if torch.cuda.is_available() else "cpu")
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

async def predict_skills(skills,X_test,llama_model,llama_tokenizer):
    predictions={}
    relevancy_array=[]
    questions=[]
    answers=[]
    for question_answer_pair in X_test:
        questions.append(question_answer_pair[0])
        answers.append(question_answer_pair[1])
        if(qnli_inference(question_answer_pair[0], question_answer_pair[1])):
            relevancy_array.append(1)
        else:
            relevancy_array.append(0)
            
    data = [{"question": question, "answer": answer} for question, answer in zip(questions, answers)]

    # Create a dataset from the combined data
    dataset = Dataset.from_dict({"question": [item["question"] for item in data], "answer": [item["answer"] for item in data]})
    for skill in skills:
        # if(skill in ["Communication","Collaboration"]):
        #     print("INSIDE ANSWER ONLY")
        #     d = {'test':Dataset.from_dict({'text1':[ex[1] for ex in X_test]})}
        #     d =DatasetDict(d)
        #     tokenized_data = d.map(preprocess_function_answer_only, batched=True)
        #     tokenized_data.set_format("torch",columns=["input_ids", "attention_mask"])
        #     data_collator = DataCollatorWithPadding(tokenizer=tokenizer)
        # else:
        #     d = {'test':Dataset.from_dict({'text1':[ex[0] for ex in X_test],'text2':[ex[1] for ex in X_test]})}
        #     d =DatasetDict(d)
        #     tokenized_data = d.map(preprocess_function, batched=True)
        #     tokenized_data.set_format("torch",columns=["input_ids", "attention_mask"])
        #     data_collator = DataCollatorWithPadding(tokenizer=tokenizer)
        
        # predictions[skill]=trained_embeddings_predictions(tokenized_data,data_collator,skill)
        predictions[skill]=get_preprocessed_data(llama_model[skill],llama_tokenizer, dataset, skill)
        for _ in range(len(predictions[skill])):
            predictions[skill][_]*=relevancy_array[_]
    return predictions