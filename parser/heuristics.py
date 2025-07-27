import re
from collections import defaultdict
import numpy as np
from .config import CONFIG

def _normalize_text_for_repetition(text):
    """Normalizes text to find repetitions (e.g., headers/footers)."""
    text = text.strip().lower()
    text = re.sub(r'\d+', '#', text)
    text = re.sub(r'\s+', ' ', text)
    return text

def filter_heading_candidates(blocks: list):
    """
    Applies a series of heuristics to filter a list of raw blocks down to
    a small set of high-quality heading candidates.
    """
    if not blocks:
        return []

    # Heuristic 1: Remove repeating headers and footers
    page_heights = defaultdict(lambda: 1000.0)
    max_y_by_page = defaultdict(float)
    for b in blocks:
        max_y_by_page[b["page"]] = max(max_y_by_page[b["page"]], b["bbox"][3])
    for p, h in max_y_by_page.items():
        page_heights[p] = h

    total_pages = len(page_heights)
    if total_pages == 0: return []

    text_counts = defaultdict(set)
    for b in blocks:
        y_center = (b["bbox"][1] + b["bbox"][3]) / 2
        page_h = page_heights[b["page"]]
        if y_center < page_h * CONFIG["header_footer_band"] or y_center > page_h * (1 - CONFIG["header_footer_band"]):
            norm_text = _normalize_text_for_repetition(b["text"])
            text_counts[norm_text].add(b["page"])

    repeating_texts = {text for text, pages in text_counts.items() if len(pages) / total_pages >= CONFIG["header_footer_frac"]}
    blocks = [b for b in blocks if _normalize_text_for_repetition(b["text"]) not in repeating_texts]

    # Heuristic 2: Filter by length
    blocks = [b for b in blocks if len(b["text"].split()) <= CONFIG["max_words"] and len(b["text"]) <= CONFIG["max_chars"]]

    if not blocks:
        return []

    # Heuristic 3: Filter by font prominence
    font_sizes = [b["font_size"] for b in blocks]
    global_font_threshold = np.percentile(font_sizes, CONFIG["global_font_pct"]) if font_sizes else 0

    page_top_fonts = defaultdict(set)
    page_fonts = defaultdict(list)
    for b in blocks:
        page_fonts[b["page"]].append(b["font_size"])
    for page, sizes in page_fonts.items():
        top_k_sizes = sorted(list(set(sizes)), reverse=True)[:CONFIG["per_page_top_k"]]
        page_top_fonts[page] = set(top_k_sizes)

    candidates = []
    for b in blocks:
        if b["font_size"] >= global_font_threshold or b["font_size"] in page_top_fonts[b["page"]]:
            candidates.append(b)
            
    return candidates
