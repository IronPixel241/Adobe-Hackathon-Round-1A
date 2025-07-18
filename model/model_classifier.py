# model/model_classifier.py
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

class HeadingClassifier:
    # Point this to the *final output* directory of the fine-tuning script
    def __init__(self, model_path="model/saved_model"):
        self.tokenizer = AutoTokenizer.from_pretrained(model_path)
        self.model = AutoModelForSequenceClassification.from_pretrained(model_path)
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model.to(self.device)
        print(f"Classifier loaded on device: {self.device}")

    def classify(self, text_list):
        if not text_list:
            return []
            
        inputs = self.tokenizer(
            text_list,
            padding=True,
            truncation=True,
            return_tensors="pt",
            max_length=512
        ).to(self.device)

        with torch.no_grad():
            logits = self.model(**inputs).logits

        predictions = torch.argmax(logits, dim=-1)
        return [self.model.config.id2label[p.item()] for p in predictions]