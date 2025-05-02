# Usage Guide for Zettelkasten-Open

This guide explains how to use Zettelkasten-Open to analyze your Obsidian notes.

## Basic Usage

After installing and setting up the tool, you can simply run:

```bash
zettelkasten-open
```

This will:

1. Read all markdown files in your configured Obsidian vault
2. Generate summaries for each note using Ollama
3. Create a "summaries" folder in your vault with individual summary files
4. Analyze connections between all summaries
5. Create a "connections.md" file with the analysis results

## Command-line Options

The tool provides several command-line options for customization:

```bash
# Run the setup wizard
zettelkasten-open --setup

# Show current configuration
zettelkasten-open --config

# Set Obsidian vault path
zettelkasten-open --vault "path/to/your/vault"

# Set Ollama model name
zettelkasten-open --model "llama3"
```

## Output Files

### Summary Files

For each note in your vault, the tool creates a corresponding summary file in the "summaries" folder. Each summary file includes:

- A header with the original filename
- The generation timestamp
- A reference to the original file path
- The AI-generated summary of the note content

### Connections File

The "connections.md" file analyzes relationships between your notes, including:

- Common themes and concepts
- Related ideas across different notes
- Potential contradictions or complementary information
- Insights that might not be obvious when reading notes individually

## Tips for Best Results

1. **Choose the right model**: More capable models like llama3 or OpenThinking-7B produce better summaries and connections
2. **Organize your notes**: Well-organized notes with clear topics lead to better connections
3. **Be patient with large vaults**: Processing many notes may take some time, especially with larger models

## Advanced Configuration

The tool stores your configuration in a JSON file at `~/.understand_yourself/config.json`. Advanced users can modify this file directly to:

- Change prompt templates
- Adjust API endpoints
- Modify output formatting

## Example Workflow

1. Write notes in Obsidian as usual
2. Periodically run `zettelkasten-open` to analyze your notes
3. Review the "connections.md" file to gain insights into your thinking
4. Use these insights to guide further note-taking and ideation
