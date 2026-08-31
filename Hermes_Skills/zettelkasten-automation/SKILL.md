---
name: zettelkasten-automation
description: Automate Zettelkasten daily note processing and sorting.
---
# Trigger conditions
Use when the user wants to process, organize, or archive daily notes/inboxes into a Zettelkasten folder structure in Obsidian or standard markdown vaults.

# Workflow
When processing a batch of daily notes (e.g., `00_Inbox/*.md`) into categorized permanent notes:
1. **Use a Python script** to automate the text parsing and file moving. Do not try to manually `cat` and `grep` dozens of files.
2. The script should:
   - Define keyword mappings for the target categories.
   - Read all `.md` files in the inbox.
   - Parse line-by-line (or block-by-block), matching keywords to categories.
   - Append the matched content to the destination files (e.g., `01_my faith/Inbox_Processed_Notes.md`).
   - Use `shutil.move` to archive the original inbox files to an `Archive` directory.
3. **File Safety:** Always ask for explicit confirmation before executing the `shutil.move` or `os.remove` operations on the user's vault files.

See `scripts/process_inbox.py` for a known-good template.