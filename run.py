import uvicorn
from transformers.modeling_outputs import TokenClassifierOutput
import torch.nn as nn

class CustomModel(nn.Module):
      def __init__(self,checkpoint,num_labels):
        super(CustomModel,self).__init__()
        self.num_labels = num_labels
    
        #Load Model with given checkpoint and extract its body
        self.model = model = AutoModel.from_pretrained(checkpoint,config=AutoConfig.from_pretrained(checkpoint, output_attentions=True,output_hidden_states=True))
        # self.model = model
    
        self.l1=nn.Linear(768, 768)
    
        # self.l2=nn.Linear(768, 768)
    
        self.dropout = nn.Dropout(0.2)
        self.classifier = nn.Linear(768,num_labels) # load and initialize weights
    
      def forward(self, input_ids=None, attention_mask=None,labels=None):
        #Extract outputs from the body
        outputs = self.model(input_ids=input_ids, attention_mask=attention_mask)
    
        #Add custom layers
        sequence_output = self.dropout(outputs[0]) #outputs[0]=last hidden state
        # print(sequence_output.shape)
        out=self.l1(sequence_output)
        # out2=self.l2(out)
        # print(out.shape)
    
        logits = self.classifier(out[:,0,:].view(-1,768)) # calculate losses
    
        # logits = self.classifier(sequence_output[:,0,:].view(-1,768)) # calculate losses
    
        loss = None
        if labels is not None:
          loss_fct = nn.CrossEntropyLoss()
          # print("here",logits.view(-1, self.num_labels),labels.view(-1))
          loss = loss_fct(logits.view(-1, self.num_labels), labels.view(-1))
    
    
    
        return TokenClassifierOutput(loss=loss, logits=logits, hidden_states=outputs.hidden_states,attentions=outputs.attentions)

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8080, reload=True)
    # uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)