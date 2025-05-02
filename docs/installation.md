# Installation Guide for Zettelkasten-Open

This guide will help you set up Zettelkasten-Open, a tool for analyzing and finding connections in your Obsidian notes.

## Prerequisites

- Python 3.6 or higher
- Ollama installed and running locally
- An Obsidian vault with notes you want to analyze

## Installing Ollama

Ollama is required to run the local LLM models that power the summarization and connection analysis.

1. Visit [ollama.ai](https://ollama.ai/) to download and install Ollama for your operating system.
2. After installation, start Ollama.
3. Pull a language model (recommended: llama3.2):
   ```bash
   ollama pull llama3.2
   ```

## Installing Zettelkasten-Open

### Method 1: From GitHub (Development)

```bash
# Clone the repository
git clone https://github.com/yourusername/zettelkasten-open.git
cd zettelkasten-open

# Install the requirements
pip install  -r Understand-Yourself\main\requirements.txt
```

### Method 2: From PyPI (Once Published)

```bash
pip install zettelkasten-open
```

## First-time Setup

After installation, run the setup wizard to configure your settings:

```bash
zettelkasten-open --setup
```

You'll need to provide:

- The path to your Obsidian vault
- The Ollama model you want to use (default: llama3)

## Troubleshooting

### Common Issues

1. **"Ollama is not running"**: Ensure Ollama is installed and running.
2. **"Model not found"**: Make sure you've pulled the model you specified:
   ```
   ollama pull <model_name>
   ```
3. **"Permission denied"**: Ensure you have write access to your Obsidian vault.

### Getting Help

If you encounter issues not covered here, please [open an issue](https://github.com/yourusername/zettelkasten-open/issues) on GitHub.
