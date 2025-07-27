"""
Central configuration for the PDF parser.
All tunable parameters and constants are defined here to allow for easy adjustments.
"""

CONFIG = {
    # Filtering repeating header/footer text
    "header_footer_frac": 0.35,
    "header_footer_band": 0.12,

    # Identifying prominent fonts
    "global_font_pct": 75, 
    "per_page_top_k": 4, 

    # Text length to filter out body paragraphs
    "max_words": 30, 
    "max_chars": 250,

    # Line merging sensitivity
    "line_merge_y_tolerance": 4.0, 
}
