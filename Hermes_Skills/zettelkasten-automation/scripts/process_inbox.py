import os
import re
import shutil

# Configuration
inbox_dir = r"C:\Users\Kreuz\Documents\SyncVault\00_Inbox"
archive_dir = r"C:\Users\Kreuz\Documents\SyncVault\Archive"
vault_dir = r"C:\Users\Kreuz\Documents\SyncVault"

categories = {
    "01_Category": [],
    "02_Category": [],
}

def categorize_line(line):
    line_lower = line.lower()
    
    # Adjust keyword matching as needed
    if any(kw in line_lower for kw in ['keyword1', 'keyword2']):
        return "01_Category"
        
    if any(kw in line_lower for kw in ['keyword3', 'keyword4']):
        return "02_Category"
        
    return None

files_processed = 0

for filename in os.listdir(inbox_dir):
    if not filename.endswith('.md'):
        continue
        
    filepath = os.path.join(inbox_dir, filename)
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()
        
    current_cat = None
    for line in lines:
        line = line.strip()
        # Skip headers or empty lines
        if not line or line.startswith('---') or line.startswith('###') or line.startswith('####') or line == '- [ ]':
            continue
            
        cat = categorize_line(line)
        if cat:
            categories[cat].append(f"- From `{filename}`: {line}")
            current_cat = cat
        elif current_cat and line.startswith('-'):
            # Append to previous category if it's a continuation
            categories[current_cat].append(f"  {line}")

    # Move to archive (WARNING: always confirm with user before automating)
    shutil.move(filepath, os.path.join(archive_dir, filename))
    files_processed += 1

# Write to destination folders
for cat, items in categories.items():
    if items:
        out_path = os.path.join(vault_dir, cat, "Inbox_Processed_Notes.md")
        with open(out_path, 'a', encoding='utf-8') as f:
            f.write("\n\n## Processed Inbox Notes\n\n")
            f.write("\n".join(items))

print(f"Processed and archived {files_processed} files.")
