---
name: windows-directory-junctions
description: Use when symlinking folders on Windows. Use mklink /J.
---

# Windows Directory Junctions

Use this skill when linking directories on Windows, particularly when linking Hermes internal directories (like `skills/`) into external synced folders (like Obsidian vaults, Google Drive, or Dropbox).

## Trigger
When asked to symlink, link, or sync a folder to another location on a Windows host.

## Context
Using standard POSIX `ln -s` inside the Hermes MSYS/bash terminal creates a Cygwin/MSYS symlink. Native Windows applications (like Obsidian, Explorer, or cloud sync engines) cannot follow these and will treat them as flat files or broken shortcuts. You MUST use a native Windows NTFS Junction instead.

## Steps
1. **Resolve Absolute Paths:** Ensure both the source and target paths are resolved as absolute Windows paths (e.g., `C:\Users\Name\Path`).
2. **Ensure Link Destination is Clear:** The junction link path itself must not already exist, but its parent directory must.
3. **Create the Junction:** Execute the command via `cmd.exe` from the terminal:
   ```bash
   cmd.exe /c "mklink /J C:\Path\To\New\Link C:\Path\To\Original\Target"
   ```
4. **Verify Two-Way Link:** Prove it is a true two-way filesystem link by checking a file's inode from both paths using `ls -i`:
   ```bash
   ls -i /c/Path/To/New/Link/file.txt /c/Path/To/Original/Target/file.txt
   ```
   If the inodes match, the junction is working perfectly and edits will flow both ways.

## Pitfalls
- **No POSIX symlinks:** Do NOT use `ln -s`.
- **Pathing:** Do not use MSYS-style paths (`/c/...`) inside the `mklink` command string; `cmd.exe` requires native Windows `C:\...` paths.
- **Safety warning:** Always warn the user not to rename or delete the linked folder from the destination application (like Obsidian), as it will break the junction or delete the source files. Remind them that editing the contents of the files is perfectly safe.