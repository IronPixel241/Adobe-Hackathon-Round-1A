# PDF Outline Extractor - Challenge 1a Solution

## Overview

This project is a robust, high-performance solution for **Challenge 1a of the Adobe India Hackathon 2025.** The primary goal is to parse PDF documents and extract a structured outline, consisting of the document's title and a hierarchical list of headings (H1, H2, H3).
Bonus: The solution also includes multilingual handling capabilities, with tested support for non-Latin scripts such as Japanese, ensuring robustness across diverse document types.



The solution is implemented as a self-contained, Dockerized Python application that operates completely offline, adheres to strict performance constraints, and is built for `linux/amd64` architecture as required. It processes all PDF files from a mounted input directory and generates a corresponding JSON file for each in an output directory, conforming to the specified schema.

---

## Our Approach

To meet the challenge's constraints (speed, no network, no large models), we opted for a **Hybrid Heuristic and Rule-Based Pipeline**. This approach avoids heavy machine learning models in favor of a fast, deterministic, and highly accurate system that analyzes a document's structural and stylistic properties.

Our solution is modular and follows a four-stage pipeline:

### 1. Raw Block Extraction (`parser/block_extractor.py`)

The first step is to read the PDF and extract all text content. Instead of a simple text dump, we extract text lines as individual "blocks," each containing rich metadata:

- The text content itself  
- Font size, name, and weight (boldness)  
- Page number  
- Bounding box coordinates (position on the page)

This detailed extraction is crucial for the subsequent heuristic analysis.

---

### 2. Heuristic Filtering (`parser/heuristics.py`)

Once we have all the raw text blocks, this module acts as a powerful filter to remove noise and significantly narrow down the content to potential headings. It applies several rules:

- **Header/Footer Removal:** Identifies and discards text that repeats across multiple pages in typical header or footer regions.  
- **Length Filtering:** Filters out excessively long lines of text, which are almost certainly body paragraphs.  
- **Font Prominence:** Analyzes font sizes used throughout the document and keeps only the text that uses a "prominent" font size (e.g., in the top 80th percentile) or is styled as bold. This dynamically adapts to each PDF's unique styling.

---

### 3. Heading Classification (`parser/classifier.py`)

The filtered "candidate" blocks are then passed to the classifier, which assigns a heading level (H1, H2, H3). To ensure accuracy and consistency, it uses a tiered logic:

- **Highest Priority (Structural Patterns):** Detects numbered lists (e.g., "1. Introduction", "2.1 Background") and assigns heading levels based on numbering.  
- **Fallback (Style-Based Mapping):** For non-numbered candidates, it uses font size. It dynamically determines the top 3 most common heading font sizes in the document and maps them to H1, H2, and H3 respectively.

---

### 4. Hierarchy Building (`parser/hierarchy_builder.py`)

The final module assembles the structured output:

- Identifies the document's **main title** (typically the largest text on the first page).  
- Organizes the classified blocks into a final JSON outline, ensuring no duplicates are included.

---

## Libraries and Models Used

Our solution is lightweight and relies on a minimal set of powerful, open-source libraries:

- [`PyMuPDF (fitz)`](https://pymupdf.readthedocs.io/en/latest/): A high-performance Python library for PDF parsing.
- `numpy`: Used for efficient numerical operations, specifically for calculating font size percentiles.

> No machine learning models are used.  
> Extremely fast, low memory usage, and fits comfortably under the 200MB constraint.

---

