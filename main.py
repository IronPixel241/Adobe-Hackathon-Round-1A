# main.py
import os
import json
from parser.extract_text_blocks import extract_text_blocks
from parser.hierarchy_builder import build_hierarchy
from model.model_classifier import HeadingClassifier

INPUT_DIR = "input"
OUTPUT_DIR = "output"

def process_pdf(pdf_path, classifier):
    # Step 1: Extract all text blocks from the PDF
    # (Your extract_text_blocks.py remains the same)
    blocks = extract_text_blocks(pdf_path)
    
    # Get the text of each block for classification
    texts_to_classify = [block['text'] for block in blocks]

    # Step 2: Use the ML model to classify all blocks in one go
    predicted_labels = classifier.classify(texts_to_classify)

    # Step 3: Add the predicted level to each block
    for block, level in zip(blocks, predicted_labels):
        # We only care about headings, so we filter out "O" (Other)
        if level != "O":
            block["level"] = level

    # Step 4: Build the final JSON hierarchy from classified blocks
    # (Your hierarchy_builder.py remains the same)
    hierarchy = build_hierarchy(blocks)
    return hierarchy

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Load the classifier once
    print("Loading the heading classification model...")
    classifier = HeadingClassifier()
    print("Model loaded successfully.")

    for filename in os.listdir(INPUT_DIR):
        if filename.lower().endswith(".pdf"):
            pdf_path = os.path.join(INPUT_DIR, filename)
            
            print(f"\nProcessing: {filename}")
            result = process_pdf(pdf_path, classifier)

            output_filename = os.path.splitext(filename)[0] + ".json"
            output_path = os.path.join(OUTPUT_DIR, output_filename)

            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(result, f, indent=4, ensure_ascii=False)

            print(f"[✓] Completed: {filename} → {output_filename}")

if __name__ == "__main__":
    main()