from transformers import AutoTokenizer, AutoModelForSequenceClassification
from transformers import pipeline

model_name = "cardiffnlp/twitter-roberta-base-sentiment"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)

classifier = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)
res = classifier("I'm feeling really sad today.")
print(res)
# [{'label': 'LABEL_0', 'score': 0.98}]  -> Negativo
