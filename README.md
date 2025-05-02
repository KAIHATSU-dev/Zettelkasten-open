# Understand Yourself - Obsidian Notes Analyzer

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
git clone https://github.com/yourusername/understand-yourself.git
cd understand-yourself

# Install the package
pip install -e .
```

Or install directly from PyPI (once published):

```bash
pip install understand-yourself
```

### Setup

Run the setup wizard to configure your vault path and model:

```bash
understand-yourself --setup
```

### Usage

Run the analyzer:

```bash
understand-yourself
```

Additional options:

```bash
# Show current configuration
understand-yourself --config

# Set Obsidian vault path
understand-yourself --vault "path/to/your/vault"

# Set Ollama model name
understand-yourself --model "llama3"
```

## Requirements

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
