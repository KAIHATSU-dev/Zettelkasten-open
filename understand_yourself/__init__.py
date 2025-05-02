import argparse
import sys
from .config import load_config, save_config
from .app import process_notes

def setup_wizard():
    """Interactive setup wizard for first-time users."""
    print("Welcome to Understand Yourself - Obsidian Notes Analyzer!")
    print("Let's set up your configuration...")
    
    config = load_config()
    
    vault_path = input(f"Enter the path to your Obsidian vault: ")
    if vault_path:
        config["obsidian_vault_path"] = vault_path
    
    model_name = input(f"Enter the Ollama model to use [default: {config['model_name']}]: ")
    if model_name:
        config["model_name"] = model_name
    
    save_config(config)
    print("Configuration saved successfully!")

def main():
    parser = argparse.ArgumentParser(description="Analyze and find connections in your Obsidian notes.")
    parser.add_argument("--setup", action="store_true", help="Run the setup wizard")
    parser.add_argument("--config", action="store_true", help="Show current configuration")
    parser.add_argument("--vault", type=str, help="Set Obsidian vault path")
    parser.add_argument("--model", type=str, help="Set Ollama model name")
    
    args = parser.parse_args()
    
    config = load_config()
    
    if args.setup:
        setup_wizard()
        return
    
    if args.config:
        print("Current Configuration:")
        for key, value in config.items():
            print(f"{key}: {value}")
        return
    
    if args.vault:
        config["obsidian_vault_path"] = args.vault
        save_config(config)
        print(f"Vault path updated to: {args.vault}")
    
    if args.model:
        config["model_name"] = args.model
        save_config(config)
        print(f"Model updated to: {args.model}")
    
    # If no vault path is set, prompt user to run setup
    if not config["obsidian_vault_path"]:
        print("No Obsidian vault path configured. Please run with --setup")
        return
    
    # Run the main application
    process_notes(config)