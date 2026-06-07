---
name: pdf
description: Read and extract text content from PDF files. Use this skill whenever the user wants to read a PDF, extract text from a PDF, or needs to access PDF content in context. Trigger on phrases like "read pdf", "extract from pdf", "pdf content", or when a .pdf file is mentioned.
---

# PDF Reader

You are a PDF reader. Extract text from PDF files using the pypdf Python library.

## Usage

When the user invokes this skill with a PDF path:

1. Use Python with pypdf to read the PDF
2. Extract and present the text content clearly
3. If pages are specified, read only those pages

## Python Code

```python
from pypdf import PdfReader
import sys

pdf_path = sys.argv[1] if len(sys.argv) > 1 else "{{path}}"

reader = PdfReader(pdf_path)
total_pages = len(reader.pages)

print(f"📄 PDF: {pdf_path}")
print(f"📑 Total pages: {total_pages}")
print()

for i, page in enumerate(reader.pages):
    print(f"\n{'='*60}")
    print(f"PAGE {i + 1}/{total_pages}")
    print('='*60)
    text = page.extract_text()
    if text.strip():
        print(text)
    else:
        print("[Empty or image-based page]")
```

Run this with: `python3 -c "..."` or save to a temp file and execute.

## Tips

- For image-based PDFs, mention that OCR would be needed
- Preserve the original structure as much as possible
- Show page numbers to help user navigate
- Handle errors gracefully (file not found, corrupted PDF, etc.)
