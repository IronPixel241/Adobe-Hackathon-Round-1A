import json

# Path to your original JSON file
json_file_path = 'train_model/data/labeled_blocks.json'  # Update this path to your JSON file

# Path to your desired output JSONL file
jsonl_file_path = 'train_model/data/labeled_data.jsonl'

# Read your original JSON file
with open(json_file_path, 'r', encoding='utf-8') as json_file:
    data = json.load(json_file)  # Loads the data

# Write to a JSON Lines file
with open(jsonl_file_path, 'w', encoding='utf-8') as jsonl_file:
    for item in data:
        jsonl_file.write(json.dumps(item, ensure_ascii=False) + '\n')

print(f"Data has been successfully converted to {jsonl_file_path}")
