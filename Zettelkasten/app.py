import os
import re
import requests
import json
from pathlib import Path
from datetime import datetime
import sys

def check_ollama_available(url):
    """Check if Ollama is running and available."""
    try:
        base_url = url.split('/api')[0]
        response = requests.get(f"{base_url}/api/tags")
        if response.status_code == 200:
            return True
        return False
    except:
        return False

def list_available_models(url):
    """List models available in Ollama."""
    try:
        base_url = url.split('/api')[0]
        response = requests.get(f"{base_url}/api/tags")
        if response.status_code == 200:
            models = response.json().get("models", [])
            return [model["name"] for model in models]
        return []
    except:
        return []

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

def get_summary_from_ollama(note_content, model_name, api_url, prompt_template):
    """Send note content to Ollama and get a summary."""
    prompt = prompt_template.format(note_content=note_content)
    
    try:
        response = requests.post(
            api_url,
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

def get_connections_between_summaries(summaries_folder, model_name, api_url, connection_prompt_template):
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
    prompt = connection_prompt_template.format(summaries_content=combined_summaries)
    
    try:
        response = requests.post(
            api_url,
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

def process_notes(config):
    """Main function to process notes with user-friendly feedback."""
    vault_path = config["obsidian_vault_path"]
    model_name = config["model_name"]
    api_url = config["ollama_api_url"]
    
    print(f"Starting to process Obsidian notes from: {vault_path}")
    
    # Check if Ollama is available
    if not check_ollama_available(api_url):
        print("Error: Ollama is not running. Please start Ollama and try again.")
        print("Installation instructions: https://github.com/ollama/ollama")
        return
    
    # Check if model is available
    available_models = list_available_models(api_url)
    if model_name not in available_models:
        print(f"Warning: Model '{model_name}' not found in Ollama.")
        if available_models:
            print(f"Available models: {', '.join(available_models)}")
        proceed = input("Do you want to proceed anyway? (y/n): ")
        if proceed.lower() != 'y':
            return
    
    # Find all markdown files
    print("Finding markdown files...")
    md_files = find_markdown_files(vault_path)
    print(f"Found {len(md_files)} markdown files")
    
    # Process each file with progress indicator
    summaries = []
    for i, file_path in enumerate(md_files):
        progress = (i+1) / len(md_files) * 100
        print(f"[{progress:.1f}%] Processing: {os.path.basename(file_path)}")
        
        # Read note content
        note_content = read_note_content(file_path)
        if not note_content:
            print(f"  Skipping empty note")
            continue
        
        # Get summary from Ollama
        print(f"  Generating summary...")
        summary = get_summary_from_ollama(note_content, model_name, api_url, 
                                         config["prompt_template"])
        
        # Add to summaries list
        summaries.append((file_path, summary))
    
    # Create summaries folder and save summaries
    summaries_folder = os.path.join(vault_path, config["summaries_folder"])
    saved_count = save_summary_to_individual_files(summaries_folder, summaries)
    print(f"Saved {saved_count} summaries to folder: {summaries_folder}")
    
    # Generate connections between summaries
    print("\nGenerating connections between summaries...")
    connections = get_connections_between_summaries(summaries_folder, model_name, 
                                                  api_url,
                                                  config["connection_prompt_template"])
    
    if connections:
        # Save connections to file
        connections_file_path = os.path.join(vault_path, config["connections_file"])
        save_connections_to_file(connections_file_path, connections)
        print(f"Connection analysis saved to: {connections_file_path}")
    else:
        print("Could not generate connections between summaries.")
    
    print("\nProcessing complete!")