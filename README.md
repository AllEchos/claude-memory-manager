# Claude Memory Manager

A command-line tool for managing conversation memories and custom memories for Claude Terminal Client.

## Features

- List all available memories (both conversation and custom memories)
- View the contents of a specific memory
- Delete a memory
- Create new custom memories with personalized instructions

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/claude-memory-manager.git
cd claude-memory-manager
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

3. Make the script executable:
```bash
chmod +x claude_memory.py
```

4. Optionally, create a symlink to make it available system-wide:
```bash
sudo ln -s $(pwd)/claude_memory.py /usr/local/bin/claude-memory
```

## Usage

### List all memories

```bash
./claude_memory.py list
```

### View a memory

```bash
# View a conversation memory (default)
./claude_memory.py view <memory_id>

# View a custom memory
./claude_memory.py view <memory_id> --type custom
```

### Delete a memory

```bash
# Delete a conversation memory (default)
./claude_memory.py delete <memory_id>

# Delete a custom memory
./claude_memory.py delete <memory_id> --type custom
```

### Create a custom memory

```bash
# Create a custom memory with inline content
./claude_memory.py create my-memory --description "My custom memory" --content "This is my custom memory content."

# Create a custom memory from a file
./claude_memory.py create my-memory --description "My custom memory" --file path/to/content.txt
```

## Memory Structure

Memories are stored in the `~/.claude_memory` directory:
- Conversation memories are stored in `~/.claude_memory/memory.json`
- Custom memories are also stored in the same file under a different key

## License

MIT

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests. 