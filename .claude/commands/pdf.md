---
description: "Read and extract text from a PDF file"
argument-hint: "FILE_PATH"
hide-from-slash-command-tool: "true"
---

# PDF Reader

Reading PDF file: $ARGUMENTS

```!python3
from pypdf import PdfReader
import sys

import os
path = "$ARGUMENTS"
if not os.path.exists(path):
    print(f"Error: File not found: {path}")
    sys.exit(1)

reader = PdfReader(path)
total_pages = len(reader.pages)

print(f"📄 PDF: {path}")
print(f"📑 Total pages: {total_pages}\n")

for i, page in enumerate(reader.pages):
    print(f"\n{'='*60}")
    print(f"PAGE {i + 1}/{total_pages}")
    print('='*60)
    text = page.extract_text()
    if text and text.strip():
        print(text)
    else:
        print("[Empty or image-based page - OCR may be needed]")
```
