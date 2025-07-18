# model/fine_tune_model.py
import torch
from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    Trainer,
    TrainingArguments,
)
from sklearn.model_selection import train_test_split
import pandas as pd
import os
from huggingface_hub import snapshot_download

# --- 1. Configuration ---
MODEL_NAME = "bert-base-uncased"
LOCAL_MODEL_DIR = "model/bert-base-uncased-local"
CACHE_DIR = "model/hub_cache"  # <-- THE FIX: A simple cache directory
OUTPUT_DIR = "model/saved_model"
TRAIN_DATA_PATH = "model/train.csv"

# --- 2. Download Model and Tokenizer (if they don't exist locally) ---
if not os.path.exists(LOCAL_MODEL_DIR):
    print(f"Downloading model and tokenizer to {LOCAL_MODEL_DIR}...")
    # ==============================================================================
    # THE FIX: Explicitly set `cache_dir` to prevent long path errors on Windows.
    # ==============================================================================
    snapshot_download(
        repo_id=MODEL_NAME,
        local_dir=LOCAL_MODEL_DIR,
        cache_dir=CACHE_DIR, # This is the critical change
        local_dir_use_symlinks=False
    )
    print("Download complete.")
else:
    print(f"Model already exists locally at {LOCAL_MODEL_DIR}")


# --- 3. Load and Prepare Data ---
df = pd.read_csv(TRAIN_DATA_PATH)
labels = sorted(df["label"].unique().tolist())
label2id = {label: i for i, label in enumerate(labels)}
id2label = {i: label for i, label in enumerate(labels)}

train_texts, eval_texts, train_labels, eval_labels = train_test_split(
    df["text"].tolist(),
    df["label"].tolist(),
    test_size=0.1,
    stratify=df["label"].tolist(),
    random_state=42
)

# --- 4. Tokenization ---
print("Loading tokenizer from local files...")
tokenizer = AutoTokenizer.from_pretrained(LOCAL_MODEL_DIR)

class PDFDataset(torch.utils.data.Dataset):
    def __init__(self, encodings, labels):
        self.encodings = encodings
        self.labels = labels

    def __getitem__(self, idx):
        item = {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}
        item['labels'] = torch.tensor(self.labels[idx])
        return item

    def __len__(self):
        return len(self.labels)

train_encodings = tokenizer(train_texts, truncation=True, padding=True, max_length=128)
eval_encodings = tokenizer(eval_texts, truncation=True, padding=True, max_length=128)

train_labels_encoded = [label2id[label] for label in train_labels]
eval_labels_encoded = [label2id[label] for label in eval_labels]

train_dataset = PDFDataset(train_encodings, train_labels_encoded)
eval_dataset = PDFDataset(eval_encodings, eval_labels_encoded)

# --- 5. Model Training ---
print("Loading model for training from local files...")
model = AutoModelForSequenceClassification.from_pretrained(
    LOCAL_MODEL_DIR,
    num_labels=len(labels),
    id2label=id2label,
    label2id=label2id
)

training_args = TrainingArguments(
    output_dir=f'{OUTPUT_DIR}/results',
    num_train_epochs=3,
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    warmup_steps=50,
    weight_decay=0.01,
    logging_dir=f'{OUTPUT_DIR}/logs',
    logging_steps=10,
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=eval_dataset,
)

print("🚀 Starting model fine-tuning...")
trainer.train()

# --- 6. Save the Fine-Tuned Model and Tokenizer ---
trainer.save_model(OUTPUT_DIR)
tokenizer.save_pretrained(OUTPUT_DIR)
print(f"✅ Model fine-tuned and saved to: {OUTPUT_DIR}")