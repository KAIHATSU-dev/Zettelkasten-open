# Updates - May 2, 2025

> **Note:** These updates are mainly generated and tracked through GitHub Copilot.

## What's New

- **Folder Selection for Summarization:**

  - The script now lists all folders in your Obsidian vault and prompts you to select a specific folder or use `-a` to summarize all folders.
  - Only markdown files in the selected folder (or all folders) are summarized.

- **Organized Output Structure:**

  - Summaries are now saved in `summaries/<FolderName>/` (or `summaries/all/` if all folders are selected).
  - Connections are saved in `connections/connections-<FolderName>.md` (or `connections/connections-all.md`).

- **Progress Bars:**

  - Added progress bars using `tqdm` for generating summaries and for reading/generating connections, providing clear visual feedback in the CLI.

- **Requirements Update:**
  - The `requirements.txt` file now includes `tqdm` for progress bar support.

---

These updates make the script more interactive, organized, and user-friendly!
