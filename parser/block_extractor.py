import fitz
from .config import CONFIG

def _merge_fragmented_lines(raw_blocks):
    """
    Post-processes raw blocks to merge text fragments that are on the same line.
    This is crucial for fixing titles and headings broken into multiple blocks.
    """
    if not raw_blocks:
        return []

    merged_blocks = []
    sorted_blocks = sorted(raw_blocks, key=lambda b: (b['page'], b['bbox'][1], b['bbox'][0]))

    if not sorted_blocks:
        return []

    current_line_block = sorted_blocks[0].copy()
    
    for i in range(1, len(sorted_blocks)):
        block = sorted_blocks[i]
        prev_bbox = current_line_block['bbox']
        curr_bbox = block['bbox']
        y_tolerance = CONFIG['line_merge_y_tolerance']

        is_same_line = (current_line_block['page'] == block['page'] and
                        abs(prev_bbox[1] - curr_bbox[1]) < y_tolerance and
                        current_line_block['font_size'] == block['font_size'] and
                        current_line_block['bold'] == block['bold'])

        if is_same_line:
            current_line_block['text'] += " " + block['text']
            new_x0 = min(prev_bbox[0], curr_bbox[0])
            new_y0 = min(prev_bbox[1], curr_bbox[1])
            new_x1 = max(prev_bbox[2], curr_bbox[2])
            new_y1 = max(prev_bbox[3], curr_bbox[3])
            current_line_block['bbox'] = (new_x0, new_y0, new_x1, new_y1)
        else:
            merged_blocks.append(current_line_block)
            current_line_block = block.copy()

    merged_blocks.append(current_line_block)

    return merged_blocks


def extract_raw_blocks(doc: fitz.Document):
    """
    Extracts all text lines from a PyMuPDF document object and merges fragments.
    """
    raw_blocks = []
    for page_num, page in enumerate(doc, start=1):
        page_blocks = page.get_text("dict", sort=True)["blocks"]
        for block in page_blocks:
            if block.get("lines"):
                for line in block["lines"]:
                    if not line.get("spans"):
                        continue
                    
                    line_text = " ".join([s["text"] for s in line["spans"]]).strip()
                    if not line_text:
                        continue
                        
                    first_span = line["spans"][0]
                    raw_blocks.append({
                        "text": line_text,
                        "font_size": round(first_span["size"], 2),
                        "font_name": first_span["font"],
                        "bold": "bold" in first_span["font"].lower(),
                        "page": page_num,
                        "bbox": line["bbox"]
                    })
    
    merged_blocks = _merge_fragmented_lines(raw_blocks)
    return merged_blocks
