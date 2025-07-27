import re

def _clean_heading_text(text):
    """Final cleaning of heading text before output."""
    return re.sub(r'\s+', ' ', text).strip()

def build_hierarchy(classified_blocks: list, all_blocks: list):
    """
    Builds the final JSON structure from the classified headings,
    handling title detection and preventing duplicates.
    """
    title = "Untitled"
    first_page_blocks = [b for b in all_blocks if b["page"] == 1]
    if first_page_blocks:
        first_page_blocks.sort(key=lambda b: (b['font_size'], -b['bbox'][1]), reverse=True)
        title = _clean_heading_text(first_page_blocks[0]['text'])

    outline = []
    seen_headings = set()

    for block in classified_blocks:
        cleaned_text = _clean_heading_text(block['text'])
        heading_key = (cleaned_text, block['page'])

        if cleaned_text and cleaned_text.lower() != title.lower() and heading_key not in seen_headings:
            outline.append({
                "level": block["level"],
                "text": cleaned_text,
                "page": block["page"]
            })
            seen_headings.add(heading_key)

    return {"title": title, "outline": outline}
