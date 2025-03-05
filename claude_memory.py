#!/usr/bin/env python3
"""
Memory Manager for Claude Terminal Client

This script allows you to manage your Claude conversation memories:
- List all available memories
- View the contents of a specific memory
- Delete a memory
- Create a new memory with custom instructions
"""

import os
import sys
import json
import argparse
from pathlib import Path
from rich.console import Console
from rich.table import Table

# Initialize console for rich text output
console = Console()

# Default memory file location
DEFAULT_MEMORY_DIR = Path.home() / ".claude_memory"
DEFAULT_MEMORY_FILE = DEFAULT_MEMORY_DIR / "memory.json"
CUSTOM_MEMORY_DIR = DEFAULT_MEMORY_DIR / "custom_memories"

def setup_memory_dirs() -> None:
    """Create the memory directories if they don't exist."""
    DEFAULT_MEMORY_DIR.mkdir(exist_ok=True)
    CUSTOM_MEMORY_DIR.mkdir(exist_ok=True)
    
    if not DEFAULT_MEMORY_FILE.exists():
        with open(DEFAULT_MEMORY_FILE, 'w') as f:
            json.dump({"conversations": {}, "custom_memories": {}}, f)

def load_memory_data() -> dict:
    """Load all memory data from file."""
    setup_memory_dirs()
    
    try:
        with open(DEFAULT_MEMORY_FILE, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return {"conversations": {}, "custom_memories": {}}

def save_memory_data(memory_data: dict) -> None:
    """Save memory data to file."""
    setup_memory_dirs()
    
    with open(DEFAULT_MEMORY_FILE, 'w') as f:
        json.dump(memory_data, f, indent=2)

def list_memories() -> None:
    """List all available memories."""
    memory_data = load_memory_data()
    
    # List conversation memories
    if memory_data["conversations"]:
        console.print("\n[bold]Conversation Memories:[/bold]")
        table = Table(show_header=True)
        table.add_column("ID", style="cyan")
        table.add_column("Messages", style="green")
        
        for memory_id, messages in memory_data["conversations"].items():
            table.add_row(memory_id, str(len(messages)))
        
        console.print(table)
    else:
        console.print("\n[bold yellow]No conversation memories found.[/bold yellow]")
    
    # List custom memories
    if memory_data.get("custom_memories", {}):
        console.print("\n[bold]Custom Memories:[/bold]")
        table = Table(show_header=True)
        table.add_column("ID", style="cyan")
        table.add_column("Description", style="green")
        
        for memory_id, memory_info in memory_data["custom_memories"].items():
            table.add_row(memory_id, memory_info.get("description", ""))
        
        console.print(table)
    else:
        console.print("\n[bold yellow]No custom memories found.[/bold yellow]")

def view_memory(memory_id: str, memory_type: str) -> None:
    """View the contents of a specific memory."""
    memory_data = load_memory_data()
    
    if memory_type == "conversation":
        if memory_id in memory_data["conversations"]:
            messages = memory_data["conversations"][memory_id]
            console.print(f"\n[bold]Conversation Memory: {memory_id}[/bold]")
            console.print(f"[bold]Number of messages: {len(messages)}[/bold]\n")
            
            for i, message in enumerate(messages):
                role = message["role"]
                content = message["content"]
                
                if role == "user":
                    console.print(f"[bold blue]User ({i+1}):[/bold blue]")
                else:
                    console.print(f"[bold green]Claude ({i+1}):[/bold green]")
                
                console.print(content)
                console.print("\n" + "-" * 80 + "\n")
        else:
            console.print(f"[bold red]Conversation memory '{memory_id}' not found.[/bold red]")
    
    elif memory_type == "custom":
        if memory_id in memory_data.get("custom_memories", {}):
            memory_info = memory_data["custom_memories"][memory_id]
            console.print(f"\n[bold]Custom Memory: {memory_id}[/bold]")
            console.print(f"[bold]Description: {memory_info.get('description', '')}[/bold]\n")
            console.print(memory_info.get("content", ""))
        else:
            console.print(f"[bold red]Custom memory '{memory_id}' not found.[/bold red]")

def delete_memory(memory_id: str, memory_type: str) -> None:
    """Delete a memory."""
    memory_data = load_memory_data()
    
    if memory_type == "conversation":
        if memory_id in memory_data["conversations"]:
            del memory_data["conversations"][memory_id]
            save_memory_data(memory_data)
            console.print(f"[bold green]Conversation memory '{memory_id}' deleted successfully.[/bold green]")
        else:
            console.print(f"[bold red]Conversation memory '{memory_id}' not found.[/bold red]")
    
    elif memory_type == "custom":
        if memory_id in memory_data.get("custom_memories", {}):
            del memory_data["custom_memories"][memory_id]
            save_memory_data(memory_data)
            console.print(f"[bold green]Custom memory '{memory_id}' deleted successfully.[/bold green]")
        else:
            console.print(f"[bold red]Custom memory '{memory_id}' not found.[/bold red]")

def create_custom_memory(memory_id: str, description: str, content_file: str = None, content: str = None) -> None:
    """Create a new custom memory."""
    memory_data = load_memory_data()
    
    if "custom_memories" not in memory_data:
        memory_data["custom_memories"] = {}
    
    if memory_id in memory_data["custom_memories"]:
        console.print(f"[bold yellow]Custom memory '{memory_id}' already exists. Updating it.[/bold yellow]")
    
    # Get content from file if provided
    if content_file:
        try:
            with open(content_file, 'r') as f:
                content = f.read()
        except Exception as e:
            console.print(f"[bold red]Error reading file {content_file}: {str(e)}[/bold red]")
            return
    
    if not content:
        console.print("[bold red]No content provided for custom memory.[/bold red]")
        return
    
    memory_data["custom_memories"][memory_id] = {
        "description": description,
        "content": content
    }
    
    save_memory_data(memory_data)
    console.print(f"[bold green]Custom memory '{memory_id}' created/updated successfully.[/bold green]")

def main():
    parser = argparse.ArgumentParser(description="Manage Claude Terminal Client memories")
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # List command
    list_parser = subparsers.add_parser("list", help="List all available memories")
    
    # View command
    view_parser = subparsers.add_parser("view", help="View the contents of a specific memory")
    view_parser.add_argument("memory_id", help="ID of the memory to view")
    view_parser.add_argument("--type", "-t", choices=["conversation", "custom"], default="conversation",
                            help="Type of memory to view (default: conversation)")
    
    # Delete command
    delete_parser = subparsers.add_parser("delete", help="Delete a memory")
    delete_parser.add_argument("memory_id", help="ID of the memory to delete")
    delete_parser.add_argument("--type", "-t", choices=["conversation", "custom"], default="conversation",
                             help="Type of memory to delete (default: conversation)")
    
    # Create command
    create_parser = subparsers.add_parser("create", help="Create a new custom memory")
    create_parser.add_argument("memory_id", help="ID for the new custom memory")
    create_parser.add_argument("--description", "-d", required=True, help="Description of the custom memory")
    create_parser.add_argument("--file", "-f", help="File containing the memory content")
    create_parser.add_argument("--content", "-c", help="Memory content as a string")
    
    args = parser.parse_args()
    
    if args.command == "list":
        list_memories()
    elif args.command == "view":
        view_memory(args.memory_id, args.type)
    elif args.command == "delete":
        delete_memory(args.memory_id, args.type)
    elif args.command == "create":
        create_custom_memory(args.memory_id, args.description, args.file, args.content)
    else:
        parser.print_help()

if __name__ == "__main__":
    main() 