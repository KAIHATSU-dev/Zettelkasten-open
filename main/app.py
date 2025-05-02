import os
import re
import requests
import json
from pathlib import Path
from datetime import datetime
from tqdm import tqdm

# Configuration
OBSIDIAN_VAULT_PATH = r"C:\Softwares\Obsidian and PF vault\VaultSync"  # Update this to your actual Obsidian vault path
OLLAMA_API_URL = "http://localhost:11434/api/generate"  # Default Ollama API URL
MODEL_NAME = "llama3.2"  # Change to the model you're using with Ollama
SUMMARIES_FOLDER = "summaries"  # Folder to store individual summaries
CONNECTIONS_FILE = "connections.md"  # File to store connections between summaries
PROMPT_TEMPLATE = "Please provide a concise summary of the following note from my Obsidian vault:\n\n{note_content}"
CONNECTION_PROMPT_TEMPLATE = "I'm looking for meaningful connections between these note summaries. Please analyze these summaries and identify key relationships, patterns, common themes, or contradictions. Here are the summaries to analyze:\n\n{summaries_content}\n\nProvide a detailed analysis of how these notes relate to each other, organized by major themes or concepts."

def find_markdown_files(vault_path):
    """Find all markdown files in the Obsidian vault."""
    md_files = []
    for root, _, files in os.walk(vault_path):
        for file in files:
            if file.endswith(".md"):
                md_files.append(os.path.join(root, file))
    return md_files

def read_note_content(file_path):
    """Read the content of a markdown file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return content
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return ""

def get_connection_from_ollama(note_content, model_name):
    """This will check all of the sumaries and try to make connections between them to better understand my brain"""
    prompt = CONNECTION_PROMPT_TEMPLATE.format(note_content=note_content)
    
    try:
        response = requests.post(
            OLLAMA_API_URL,
            json={
                "model": model_name,
                "prompt": prompt,
                "stream": False
            }
        )
        
        if response.status_code == 200:
            result = response.json()
            return result.get("response", "No connection generated")
        else:
            print(f"Error from Ollama API: {response.status_code}, {response.text}")
            return f"Failed to generate connection (Error: {response.status_code})"
    except Exception as e:
        print(f"Exception when calling Ollama API: {e}")
        return f"Failed to generate connection due to error: {str(e)}"

def get_summary_from_ollama(note_content, model_name):
    """Send note content to Ollama and get a summary."""
    prompt = PROMPT_TEMPLATE.format(note_content=note_content)
    
    try:
        response = requests.post(
            OLLAMA_API_URL,
            json={
                "model": model_name,
                "prompt": prompt,
                "stream": False
            }
        )
        
        if response.status_code == 200:
            result = response.json()
            return result.get("response", "No summary generated")
        else:
            print(f"Error from Ollama API: {response.status_code}, {response.text}")
            return f"Failed to generate summary (Error: {response.status_code})"
    except Exception as e:
        print(f"Exception when calling Ollama API: {e}")
        return f"Failed to generate summary due to error: {str(e)}"

def save_summary_to_individual_files(summaries_folder, summaries):
    """Save each summary to an individual markdown file in the summaries folder."""
    # Create summaries folder if it doesn't exist
    os.makedirs(summaries_folder, exist_ok=True)
    
    # Count of successfully saved summaries
    saved_count = 0
    
    for note_path, summary in summaries:
        try:
            # Create a clean filename from the original note name
            original_filename = os.path.basename(note_path)
            # Keep the original extension
            summary_filename = original_filename
            summary_path = os.path.join(summaries_folder, summary_filename)
            
            with open(summary_path, 'w', encoding='utf-8') as f:
                f.write(f"# Summary of {original_filename}\n\n")
                f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                f.write(f"**Original file:** `{note_path}`\n\n")
                f.write(f"## Summary\n\n{summary}\n\n")
            
            saved_count += 1
            print(f"Saved summary to: {summary_path}")
        except Exception as e:
            print(f"Error saving summary for {note_path}: {e}")
    
    return saved_count

def get_connections_between_summaries(summaries_folder, model_name):
    """Generate connections between summaries using Ollama."""
    print("Reading all summaries to find connections...")
    
    # Read all summary files
    summaries_content = []
    summary_files = []
    
    for root, _, files in os.walk(summaries_folder):
        for file in files:
            if file.endswith(".md"):
                file_path = os.path.join(root, file)
                summary_files.append(file_path)
                
    # Read each summary file
    for file_path in summary_files:
        content = read_note_content(file_path)
        if content:
            summaries_content.append(f"Summary of {os.path.basename(file_path)}:\n{content}\n")
    
    if not summaries_content:
        print("No summaries found to analyze.")
        return None
    
    # Combine summaries for the prompt (may need to batch for large numbers of summaries)
    combined_summaries = "\n---\n".join(summaries_content)
    
    # Send to Ollama for connection analysis
    print(f"Analyzing connections between {len(summaries_content)} summaries...")
    prompt = CONNECTION_PROMPT_TEMPLATE.format(summaries_content=combined_summaries)
    
    try:
        response = requests.post(
            OLLAMA_API_URL,
            json={
                "model": model_name,
                "prompt": prompt,
                "stream": False
            }
        )
        
        if response.status_code == 200:
            result = response.json()
            connections = result.get("response", "No connections found between summaries.")
            return connections
        else:
            print(f"Error from Ollama API: {response.status_code}, {response.text}")
            return f"Failed to generate connections (Error: {response.status_code})"
    except Exception as e:
        print(f"Exception when calling Ollama API: {e}")
        return f"Failed to generate connections due to error: {str(e)}"

def save_connections_to_file(connections_file_path, connections):
    """Save the connections analysis to a markdown file."""
    try:
        with open(connections_file_path, 'w', encoding='utf-8') as f:
            f.write(f"# Connections Between Notes\n\n")
            f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write(f"## Analysis\n\n{connections}\n\n")
        
        print(f"Connections saved to: {connections_file_path}")
        return True
    except Exception as e:
        print(f"Error saving connections to file: {e}")
        return False

def list_folders_in_vault(vault_path):
    """List all folders in the Obsidian vault (excluding hidden/system folders)."""
    folders = []
    for entry in os.scandir(vault_path):
        if entry.is_dir() and not entry.name.startswith('.'):
            folders.append(entry.name)
    return folders

def main():
    print(f"Starting to process Obsidian notes from: {OBSIDIAN_VAULT_PATH}")

    # List all folders in the vault
    folders = list_folders_in_vault(OBSIDIAN_VAULT_PATH)
    print("\nFolders found in the vault:")
    for idx, folder in enumerate(folders, 1):
        print(f"  {idx}. {folder}")
    print("\nEnter the folder name to summarize, or '-a' to summarize all folders:")
    selected = input().strip()

    if selected == "-a":
        search_path = OBSIDIAN_VAULT_PATH
        folder_label = "all"
        print("Summarizing all folders...")
    elif selected in folders:
        search_path = os.path.join(OBSIDIAN_VAULT_PATH, selected)
        folder_label = selected
        print(f"Summarizing only folder: {selected}")
    else:
        print("Invalid selection. Exiting.")
        return

    # Find all markdown files in the selected folder or all folders
    md_files = find_markdown_files(search_path)
    print(f"Found {len(md_files)} markdown files")

    summaries_folder = os.path.join(OBSIDIAN_VAULT_PATH, SUMMARIES_FOLDER, folder_label)
    os.makedirs(summaries_folder, exist_ok=True)

    summaries = []
    for i, file_path in enumerate(tqdm(md_files, desc="Generating summaries")):
        print(f"Processing {i+1}/{len(md_files)}: {file_path}")
        note_content = read_note_content(file_path)
        if not note_content:
            print(f"Skipping empty note: {file_path}")
            continue
        print(f"Generating summary via Ollama ({MODEL_NAME})...")
        summary = get_summary_from_ollama(note_content, MODEL_NAME)
        summaries.append((file_path, summary))
        print(f"Summary generated successfully.")

    saved_count = save_summary_to_individual_files(summaries_folder, summaries)
    print(f"All done! Saved {saved_count} summaries to folder: {summaries_folder}")

    print("\nNow generating connections between summaries...")
    from glob import glob
    summary_files = [y for x in os.walk(summaries_folder) for y in glob(os.path.join(x[0], '*.md'))]
    summaries_content = []
    for file_path in tqdm(summary_files, desc="Reading summaries for connections"):
        content = read_note_content(file_path)
        if content:
            summaries_content.append(f"Summary of {os.path.basename(file_path)}:\n{content}\n")
    if not summaries_content:
        print("No summaries found to analyze.")
        return
    combined_summaries = "\n---\n".join(summaries_content)
    print("Analyzing connections...")
    prompt = CONNECTION_PROMPT_TEMPLATE.format(summaries_content=combined_summaries)
    try:
        with tqdm(total=1, desc="Generating connections") as pbar:
            response = requests.post(
                OLLAMA_API_URL,
                json={
                    "model": MODEL_NAME,
                    "prompt": prompt,
                    "stream": False
                }
            )
            pbar.update(1)
        if response.status_code == 200:
            result = response.json()
            connections = result.get("response", "No connections found between summaries.")
        else:
            print(f"Error from Ollama API: {response.status_code}, {response.text}")
            connections = f"Failed to generate connections (Error: {response.status_code})"
    except Exception as e:
        print(f"Exception when calling Ollama API: {e}")
        connections = f"Failed to generate connections due to error: {str(e)}"

    connections_folder = os.path.join(OBSIDIAN_VAULT_PATH, "connections")
    os.makedirs(connections_folder, exist_ok=True)
    connections_file_path = os.path.join(connections_folder, f"connections-{folder_label}.md")
    if connections:
        save_connections_to_file(connections_file_path, connections)
        print(f"Connection analysis complete and saved to {connections_file_path}")
    else:
        print("Could not generate connections between summaries.")

    print("\nAll processing complete!")

if __name__ == "__main__":
    main()