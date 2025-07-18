# model/create_dataset.py
import csv

def create_training_data():
    """Generates a synthetic but representative dataset for training."""
    data = [
        # H1 Examples
        ("1. Introduction", "H1"),
        ("2. Background and Motivation", "H1"),
        ("CHAPTER I: THE BEGINNING", "H1"),
        ("Executive Summary", "H1"),
        ("Abstract", "H1"),

        # H2 Examples
        ("1.1 System Architecture", "H2"),
        ("2.1 Related Work", "H2"),
        ("Key Findings", "H2"),
        ("Methodology", "H2"),
        ("Results and Discussion", "H2"),

        # H3 Examples
        ("1.1.1 Data Preprocessing", "H3"),
        ("2.1.1 Previous Models", "H3"),
        ("Limitations:", "H3"),
        ("Future Work:", "H3"),
        ("Statistical Analysis", "H3"),

        # Paragraph Text (Other)
        ("This paper presents a novel approach to document understanding.", "O"),
        ("The quick brown fox jumps over the lazy dog.", "O"),
        ("As shown in Figure 3, the results indicate a significant improvement.", "O"),
        ("All rights reserved. This document is confidential.", "O"),
        ("For more information, please contact the authors.", "O"),
        ("The data was collected over a period of six months.", "O"),
        ("We used a standard dataset for our evaluation.", "O")
    ]
    
    # Duplicate data to make the dataset larger and more robust
    multiplied_data = data * 50

    # Write to CSV
    output_path = "model/train.csv"
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["text", "label"])
        writer.writerows(multiplied_data)
        
    print(f"✅ Successfully created training dataset at: {output_path}")

if __name__ == "__main__":
    create_training_data()