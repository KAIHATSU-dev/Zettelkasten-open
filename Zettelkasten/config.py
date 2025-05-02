import os
import json
from pathlib import Path

DEFAULT_CONFIG = {
    "obsidian_vault_path": "",
    "ollama_api_url": "http://localhost:11434/api/generate",
    "model_name": "llama3",
    "summaries_folder": "summaries",
    "connections_file": "connections.md",
    "prompt_template": "Please provide a concise summary of the following note from my Obsidian vault:\n\n{note_content}",
    "connection_prompt_template": "I'm looking for meaningful connections between these note summaries. Please analyze these summaries and identify key relationships, patterns, common themes, or contradictions. Here are the summaries to analyze:\n\n{summaries_content}\n\nProvide a detailed analysis of how these notes relate to each other, organized by major themes or concepts."
}

def get_config_path():
    """Get the path to the config file."""
    # Use user's home directory for config
    home = Path.home()
    config_dir = home / ".understand_yourself"
    config_dir.mkdir(exist_ok=True)
    return config_dir / "config.json"

def load_config():
    """Load configuration from file or create default."""
    config_path = get_config_path()
    
    if config_path.exists():
        with open(config_path, 'r') as f:
            return json.load(f)
    else:
        # First-time setup - create default config
        save_config(DEFAULT_CONFIG)
        return DEFAULT_CONFIG

def save_config(config):
    """Save configuration to file."""
    config_path = get_config_path()
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=2)