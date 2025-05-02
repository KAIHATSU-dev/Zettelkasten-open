# Zettelkasten-Open - Obsidian Notes Analyzer

A tool to analyze your Obsidian vault notes, create summaries, and discover meaningful connections between your ideas.

## Features

- Automatically summarizes all notes in your Obsidian vault
- Creates individual summary files for each note
- Analyzes connections between notes to find patterns and relationships
- Works with local LLM models through Ollama

## Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/zettelkasten-open.git
cd zettelkasten-open

# A virtual envionrment is highly recommended
python -m venv 'name of virtual enviornment'

example:
python -m venv venv
.\venv\Scripts\activate

# activate the virtual enviornment


# Install the package
pip install -r requirements.txt
```

### Usage

Run the analyzer:

## Requirements

- Obsidian
- Python 3.6+
- Ollama installed and running locally

## How It Works

1. The tool scans your Obsidian vault for all markdown notes
2. Each note is sent to Ollama for summarization
3. Summaries are saved to a "summaries" folder in your vault
4. All summaries are analyzed together to find connections
5. A "connections.md" file is created with the analysis

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
