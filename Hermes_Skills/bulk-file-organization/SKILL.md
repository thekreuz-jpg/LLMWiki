---
name: bulk-file-organization
description: Use to organize, rename, or sort large file directories.
---
# Trigger Conditions
Use when the user asks to organize, sort, rename, or categorize massive directories of files, especially large PDFs, media, or mixed downloads.

# Workflow & Pitfalls
- **Avoid Heavy Extraction:** Do not attempt to OCR, read, or extract text from gigabytes of PDFs or images just to determine their title or category. It will hit execution timeouts, waste tokens, and produce garbage file names (e.g., `Table of Contents.pdf`).
- **Use Filenames First:** Write a Python script to parse existing filenames. Most downloaded files already contain the title and subject within the string.
- **Clean Junk Strings:** Use string replacement and regex to strip common internet download junk (e.g., `_OceanofPDF.com_`, `pdfcoffee.com_`, `-pdf-free`, `_abbyy.gz`, underscores instead of spaces).
- **Categorize via Keywords:** Map relevant keywords to category folders and move files into subdirectories based on filename matches.
- **Handle Collisions:** Always implement a counter `(1)` for duplicate filenames when moving files to avoid overwriting.
- **Get Permission:** Always get explicit user approval before executing a script that moves or renames bulk files (File Safety Hard Stop).