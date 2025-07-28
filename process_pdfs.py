import os
import json
import time
import fitz  
from pathlib import Path
 
from parser.block_extractor import extract_raw_blocks
from parser.heuristics import filter_heading_candidates
from parser.classifier import classify_candidates
from parser.hierarchy_builder import build_hierarchy

def process_pdf(pdf_path: str):
    """
    Main pipeline to process a single PDF file by orchestrating the modular components.
    """
    try:
        doc = fitz.open(pdf_path)
    except Exception as e:
        print(f"    Error opening {os.path.basename(pdf_path)}: {e}")
        return None
     
    all_blocks = extract_raw_blocks(doc)
    candidates = filter_heading_candidates(all_blocks)
    classified_blocks = classify_candidates(candidates)
    result = build_hierarchy(classified_blocks, all_blocks)
    
    doc.close()
    return result

def main():
    """
    Main execution function for the Docker container.
    Reads all PDFs from /app/input and writes JSONs to /app/output.
    """ 
    INPUT_DIR = Path("/app/input")
    OUTPUT_DIR = Path("/app/output")
     
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    print("Starting PDF processing...")
    print(f"Reading files from: {INPUT_DIR}")
    print(f"Writing output to: {OUTPUT_DIR}")
    
    pdf_files = list(INPUT_DIR.glob("*.pdf"))
    
    if not pdf_files:
        print("No PDF files found in the input directory.")
    else:
        print(f"Found {len(pdf_files)} PDF file(s) to process.")
        for pdf_path in pdf_files:
            filename = pdf_path.name
            output_filename = f"{pdf_path.stem}.json"
            output_path = OUTPUT_DIR / output_filename
            
            print(f"  - Processing '{filename}'...")
            start_time = time.time()
            
            try:
                result_json = process_pdf(str(pdf_path))
                
                if result_json:
                    with open(output_path, "w", encoding="utf-8") as f:
                        json.dump(result_json, f, indent=4, ensure_ascii=False)
                    
                    exec_time = time.time() - start_time
                    print(f"  Output saved to '{output_path.name}' in {exec_time:.2f}s")

            except Exception as e:
                print(f"   Critical error processing '{filename}': {e}")
    
    print("Processing complete.")

if __name__ == "__main__":
    main()
