---
name: pdf
description: Read and extract text content from PDF files
arguments:
  - name: path
    description: Path to the PDF file to read
    required: true
  - name: pages
    description: Optional page range (e.g., "1-5", "3", "1-3,5-7")
    required: false
---

You are a PDF reader. The user wants to read the PDF file at: {{path}}

{{#if pages}}
Reading pages: {{pages}}
{{/if}}

Please use Python with pypdf to:
1. Open the PDF file at the given path
2. Extract text from the requested pages (or all pages if not specified)
3. Present the content in a clear, readable format

Use this Python code:

```python
from pypdf import PdfReader

reader = PdfReader("{{path}}")

{{#if pages}}
# Parse page range
def parse_page_range(range_str, total_pages):
    pages = []
    for part in range_str.split(','):
        if '-' in part:
            start, end = part.split('-')
            pages.extend(range(int(start)-1, int(end)))
        else:
            pages.append(int(part)-1)
    return [p for p in pages if 0 <= p < total_pages]

pages_to_read = parse_page_range("{{pages}}", len(reader.pages))
total = len(pages_to_read)
print(f"Reading {total} page(s) from PDF (total {len(reader.pages)} pages)")
for i, page_num in enumerate(pages_to_read):
    page = reader[page_num]
    print(f"\n--- Page {page_num + 1} ---")
    print(page.extract_text())
{{else}}
print(f"Reading {len(reader.pages)} pages from PDF")
for i, page in enumerate(reader.pages):
    print(f"\n--- Page {i + 1} ---")
    print(page.extract_text())
{{/if}}
```

Run this code using the Bash tool with python -c and provide the extracted content to the user.
