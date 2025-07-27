import re

def classify_candidates(candidates: list):
    """
    Classifies a list of candidate blocks, assigning a heading level to each.
    Prioritizes structural patterns over style and avoids classifying stray numbers.
    """
    if not candidates:
        return []

    candidate_font_sizes = sorted(list(set(c['font_size'] for c in candidates)), reverse=True)
    size_to_level = {size: f"H{i+1}" for i, size in enumerate(candidate_font_sizes[:3])}

    classified_blocks = []
    for block in candidates:
        text = block['text'].strip()
        level = None

        match = re.match(r'^\d+(\.\d+)*\s*(.*)', text)
        if match and match.group(2):
            dots = match.group(0).count('.')
            level = f"H{dots}"

        if level is None:
            level_from_style = size_to_level.get(block['font_size'])
            if level_from_style:
                if not text.endswith('.') and len(text.split()) < 20 and not text.isnumeric():
                    level = level_from_style

        if level:
            block['level'] = level
            classified_blocks.append(block)
    
    return classified_blocks
