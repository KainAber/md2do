# md2do

> **⚠️ Work in Progress / Proof of Concept**  
> This project is actively being developed and may have incomplete features or breaking changes.

A **speech-to-LLM todo.md updater** that allows you to manage your todo list using natural language voice commands and AI assistance.

## What is md2do?

md2do is a Python application that combines:
- **Voice input/output** for hands-free todo management
- **AI-powered task manipulation** using OpenAI's language models
- **Git version control** for tracking all changes
- **Markdown-based todo lists** for easy editing and viewing

## Features

- 🎤 **Voice Input**: Speak your todo updates naturally
- 🤖 **AI Assistant**: Uses OpenAI to understand and execute complex commands
- 📝 **Smart Todo Management**: Add, edit, delete, move, and reorganize tasks
- 🔄 **Git Integration**: Automatic commits and rollback capabilities
- 📱 **View Creation**: Filter and create custom views of your todos
- 🔊 **Text-to-Speech**: Hear back what changes were made

## Quick Start

1. **Install dependencies**:
   ```bash
   uv sync
   ```

2. **Set up OpenAI configuration**:
   Create an `openai_api_config.yml` file with your OpenAI API key:
   ```yaml
   api key: <your-api-key-here>
   ```

3. **Run the application**:
   ```bash
   uv run main.py
   ```

4. **Start speaking** your todo updates!

## Usage Examples

- "Add a new task to buy groceries"
- "Reorder bugs alphabetically"
- "Mark the task on view creation as bold"
- "Rollback my last change"

## Project Structure

```
md2do/
├── main.py              # Main application entry point
├── src/
│   ├── functions.py     # Core todo manipulation functions
│   ├── utils.py         # Utility functions and OpenAI integration
│   └── voice_input.py   # Speech recognition and TTS
├── prompts/             # AI prompt templates
└── todo.md              # Your main todo list
```

## Requirements

- Python 3.8.1+
- OpenAI API key
- Microphone and speakers
- Git repository (for version control)

## Dependencies

- `openai` - OpenAI API integration
- `SpeechRecognition` - Voice input processing
- `pygame` & `pydub` - Audio playback
- `openai-whisper` - Speech-to-text
- `pyaudio` - Audio I/O

## Future Developments

This project is actively developed with many features planned. Check the [`todo.md`](todo.md) file for the current feature backlog.
