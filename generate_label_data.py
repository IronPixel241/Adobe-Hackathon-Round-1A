import json
from parser.extract_text_blocks import extract_text_blocks

def export_for_labeling(pdf_path, output_json_path):
    blocks = extract_text_blocks(pdf_path)

    # Prepare data with empty labels for manual annotation
    labeled_blocks = []
    for b in blocks:
        labeled_blocks.append({
            "text": b["text"],
            "font_size": b["font_size"],
            "bold": b["bold"],
            "page": b["page"],
            "label": ""  # <-- To be filled manually: e.g. H1, H2, H3, O, etc.
        })

    with open(output_json_path, "w", encoding="utf-8") as f:
        json.dump(labeled_blocks, f, indent=4, ensure_ascii=False)
    print(f"Exported {len(labeled_blocks)} blocks to {output_json_path}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: python export_labeling_json.py <input_pdf_path> <output_json_path>")
    else:
        pdf_path = sys.argv[1]
        output_json_path = sys.argv[2]
        export_for_labeling(pdf_path, output_json_path)
