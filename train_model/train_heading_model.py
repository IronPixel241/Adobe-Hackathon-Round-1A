from transformers import AutoTokenizer, AutoModelForSequenceClassification, Trainer, TrainingArguments
import datasets
import os

LABELS = ["O", "H1", "H2", "H3", "H4"]

tokenizer = AutoTokenizer.from_pretrained("huawei-noah/TinyBERT_General_4L_312D")

# Set padding and truncation during tokenization
def preprocess_data(example):
    # Ensure the text is properly tokenized with padding and truncation
    return tokenizer(example['text'], padding='max_length', truncation=True, max_length=512)

def label_to_id(example):
    """
    Convert label to the corresponding index in the LABELS list.
    Ensures that labels are integers (index-based).
    """
    # If there's no label or empty label, default to "O"
    if example['label'] == "":
        example['label'] = "O"
    # Convert label to the corresponding index in the LABELS list
    example['label'] = LABELS.index(example['label'])  # Convert label to integer index
    return example

def main():
    data_files = {
        "train": "train_model/data/labeled_data.jsonl"
    }

    # Ensure validation data exists
    if os.path.exists("train_model/data/valid.jsonl"):
        data_files["validation"] = "train_model/data/valid.jsonl"

    # Load dataset
    dataset = datasets.load_dataset("json", data_files=data_files)

    # Convert labels to IDs
    dataset = dataset.map(label_to_id)

    # Tokenize the dataset using the tokenizer
    dataset = dataset.map(preprocess_data, batched=True)

    # Load the model with the appropriate number of labels
    model_name = "huawei-noah/TinyBERT_General_4L_312D"
    model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=len(LABELS))

    # Training arguments
    training_args = TrainingArguments(
        output_dir="train_model/model/trained_model",  # Save the model here
        save_strategy="epoch",  # Save the model after each epoch
        learning_rate=2e-5,
        per_device_train_batch_size=16,
        per_device_eval_batch_size=32,
        num_train_epochs=3,
        weight_decay=0.01,
        save_total_limit=1,
        logging_dir="train_model/model/trained_model/logs",  # Logs directory
        logging_steps=10,
        # Removed evaluation_strategy to avoid the error
    )

    # Initialize the Trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=dataset["train"],
        eval_dataset=dataset.get("validation", None),
        tokenizer=tokenizer
    )

    # Train the model
    trainer.train()

    # Save the trained model and tokenizer
    trainer.save_model("train_model/model/trained_model")
    tokenizer.save_pretrained("train_model/model/trained_model")

    print("✅ Model training complete. Saved to 'train_model/model/trained_model' folder.")

if __name__ == "__main__":
    main()
