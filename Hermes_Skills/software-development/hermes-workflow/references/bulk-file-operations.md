# Bulk File Operations & Categorization

When tasked with organizing, categorizing, or renaming a large directory of files (e.g., 50+ files, or GBs of PDFs/documents):

1. **Avoid Content Parsing:** Do NOT attempt to read the file contents (e.g., OCRing the first pages of PDFs, or reading full markdown files) to determine categories. It is slow, highly prone to LLM context limits, and will hit execution timeouts.
2. **Leverage Filenames & Heuristics:** Parse the existing filenames using regex and keyword matching. Most user downloads and notes already contain the subject in the filename or in predictable structured headers.
3. **Prefer Python Scripts:** Write a Python script using `os`, `re`, and `shutil` to perform the operations instead of relying on Bash `find`/`mv`/`grep` loops. Python handles Windows paths, spaces, special characters, and complex collision logic (e.g., appending `(1)` to duplicates) much more safely.
4. **Hard Stop for Moves/Renames:** Always present the categorization plan to the user and get explicit approval before executing any destructive `shutil.move`, `os.rename`, or `os.remove` operations.