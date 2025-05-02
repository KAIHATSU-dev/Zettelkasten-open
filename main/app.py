import os
import re
import requests
import json
from pathlib import Path
from datetime import datetime

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

def main():
    print(f"Starting to process Obsidian notes from: {OBSIDIAN_VAULT_PATH}")
    
    # Find all markdown files
    md_files = find_markdown_files(OBSIDIAN_VAULT_PATH)
    print(f"Found {len(md_files)} markdown files")
    
    # Process each file
    summaries = []
    for i, file_path in enumerate(md_files):
        print(f"Processing {i+1}/{len(md_files)}: {file_path}")
        
        # Read note content
        note_content = read_note_content(file_path)
        if not note_content:
            print(f"Skipping empty note: {file_path}")
            continue
        
        # Get summary from Ollama
        print(f"Generating summary via Ollama ({MODEL_NAME})...")
        summary = get_summary_from_ollama(note_content, MODEL_NAME)
        
        # Add to summaries list
        summaries.append((file_path, summary))
        print(f"Summary generated successfully.")
    
    # Create summaries folder
    summaries_folder = os.path.join(OBSIDIAN_VAULT_PATH, SUMMARIES_FOLDER)
    saved_count = save_summary_to_individual_files(summaries_folder, summaries)
    print(f"All done! Saved {saved_count} summaries to folder: {summaries_folder}")
    
    # Generate connections between summaries
    print("\nNow generating connections between summaries...")
    connections = get_connections_between_summaries(summaries_folder, MODEL_NAME)
    
    if connections:
        # Save connections to file
        connections_file_path = os.path.join(OBSIDIAN_VAULT_PATH, CONNECTIONS_FILE)
        save_connections_to_file(connections_file_path, connections)
        print(f"Connection analysis complete and saved to {connections_file_path}")
    else:
        print("Could not generate connections between summaries.")
    
    print("\nAll processing complete!")

if __name__ == "__main__":
    main()