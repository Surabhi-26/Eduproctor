from transformers import BertForSequenceClassification, BertTokenizer
import torch
import os

# Set the HF_HUB_DISABLE_SYMLINKS_WARNING environment variable to '1'
os.environ['HF_HUB_DISABLE_SYMLINKS_WARNING'] = '1'

# Load pre-trained BERT model and tokenizer
model_name = "bert-base-uncased"
tokenizer = BertTokenizer.from_pretrained(model_name)
model = BertForSequenceClassification.from_pretrained(model_name)

# Define input question and answer
question = "What is the capital of France?"
answer = "Paris"

# Concatenate question and answer with [SEP] token
input_text = f"{question} [SEP] {answer}"

# Tokenize input text
inputs = tokenizer(input_text, return_tensors="pt", padding=True, truncation=True)

# Feed input to the model
outputs = model(**inputs)

# Process model outputs
logits = outputs.logits
predicted_class = torch.argmax(logits, dim=1).item()

# Interpret model predictions
predicted_label = "true" if predicted_class == 1 else "false"

# Print results
print("Question:", question)
print("Answer:", answer)
print("Does the answer match the question?", predicted_label)
