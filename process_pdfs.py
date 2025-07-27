import os
import json
import time
import fitz

from parser.block_extractor import extract_raw_blocks
from parser.heuristics import filter_heading_candidates
from parser.classifier import classify_candidates
from parser.hierarchy_builder import build_hierarchy

def process_pdf(pdf_path: str):
    """
    Main pipeline to process a single PDF file by orchestrating the modular components.
    """
    doc = fitz.open(pdf_path)
    
    all_blocks = extract_raw_blocks(doc)
    candidates = filter_heading_candidates(all_blocks)
    classified_blocks = classify_candidates(candidates)
    result = build_hierarchy(classified_blocks, all_blocks)
    
    doc.close()
    return result

if __name__ == "__main__":
    INPUT_DIR = "/sample_dataset/pdfs"
    OUTPUT_DIR = "/sample_dataset/outputs"
    os.makedirs(INPUT_DIR, exist_ok=True)
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    pdf_files = [f for f in os.listdir(INPUT_DIR) if f.lower().endswith(".pdf")]
    
    if not pdf_files:
        print(f"No PDF files found in the '{INPUT_DIR}' directory. Please add a PDF to process.")
    else:
        for filename in pdf_files:
            pdf_path = os.path.join(INPUT_DIR, filename)
            output_filename = os.path.splitext(filename)[0] + ".json"
            output_path = os.path.join(OUTPUT_DIR, output_filename)
            
            print(f"Processing '{filename}'...")
            start_time = time.time()
            
            try:
                result_json = process_pdf(pdf_path)
                
                with open(output_path, "w", encoding="utf-8") as f:
                    json.dump(result_json, f, indent=4, ensure_ascii=False)
                
                exec_time = time.time() - start_time
                print(f"Output saved to '{output_path}' in {exec_time:.2f}s")

            except Exception as e:
                print(f"Error processing '{filename}': {e}")
