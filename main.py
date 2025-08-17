from src.utils import (
    get_system_prompt,
    get_user_prompt,
    get_openai_config,
    create_openai_client,
    load_function_schemas,
    load_functions_module,
    get_todo_md,
    format_numbered_todo,
    fill_system_prompt,
    fill_user_prompt,
    get_user_input,
    get_model_response,
    has_function_call,
    get_function_details,
    execute_function_call,
    get_clean_git_diff,
    display_model_response_with_tts,
    get_git_diff,
    add_function_call_to_messages,
    commit_todo_changes,
    logger,
)
import yaml
import subprocess
from datetime import datetime
from pynput import keyboard
import os
from src.voice_input import get_voice_input

# Global variables for keyboard monitoring
keys = set()
listening_enabled = False
keyboard_listener = None

def new_md():
    """Create a new markdown file with timestamp in md/inbox directory"""
    timestamp = datetime.now().strftime("%Y-%m-%d--%H-%M-%S")
    filename = f"{timestamp}.md"
    
    # Create md/inbox directory if it doesn't exist
    inbox_dir = "md/inbox"
    os.makedirs(inbox_dir, exist_ok=True)
    
    # Create the file path
    file_path = os.path.join(inbox_dir, filename)
    
    # Create an empty markdown file
    with open(file_path, 'w') as f:
        f.write(f"# {timestamp}\n\n")
    
    logger.info(f"Created new markdown file: {file_path}")
    
    # Open Terminal and navigate to inbox directory, then open file in neovim
    subprocess.run(["open", "-a", "Terminal", os.path.expanduser("~")], capture_output=True)
    subprocess.run(["osascript", "-e", f'tell application "Terminal" to do script "cd {os.path.abspath(inbox_dir)} && nvim {filename}" in front window'], capture_output=True)

def toggle_listening():
    """Toggle voice listening on/off"""
    global listening_enabled
    listening_enabled = not listening_enabled
    status = "enabled" if listening_enabled else "disabled"
    logger.info(f"Voice listening {status}")

def on_press(key):
    """Handle key press events"""
    key_str = key.name if hasattr(key, 'name') else str(key)
    keys.add(key_str)
    check_shortcuts()

def on_release(key):
    """Handle key release events"""
    key_str = key.name if hasattr(key, 'name') else str(key)
    keys.discard(key_str)

def check_shortcuts():
    """Check if any keyboard shortcuts are triggered"""
    try:
        with open("keyboard_shortcuts.yaml", "r") as f:
            config = yaml.safe_load(f)
        
        for shortcut_name, shortcut in config["shortcuts"].items():
            if set(shortcut["keys"]).issubset(keys):
                if shortcut_name == "new_md":
                    new_md()
                elif shortcut_name == "toggle_listening":
                    toggle_listening()
                keys.clear()
                break
    except Exception as e:
        logger.error(f"Error checking shortcuts: {e}")

def start_keyboard_monitor():
    """Start the keyboard monitoring"""
    global keyboard_listener
    keyboard_listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    keyboard_listener.start()
    logger.info("Keyboard monitoring started")

def stop_keyboard_monitor():
    """Stop the keyboard monitoring"""
    global keyboard_listener
    if keyboard_listener:
        keyboard_listener.stop()
        logger.info("Keyboard monitoring stopped")

def get_user_input_with_voice():
    """Get user input, with voice input as fallback if listening is enabled"""
    # If voice listening is enabled, try voice input first
    if listening_enabled:
        logger.info("Voice listening enabled, trying voice input...")
        voice_input = get_voice_input()
        if voice_input:
            logger.info(f"Voice input received: {voice_input}")
            return voice_input
        else:
            logger.info("No voice input detected, falling back to text input")
    
    # Fallback to text input
    return input("> ").strip()

def app():
    system_prompt_template = get_system_prompt()
    user_prompt_template = get_user_prompt()
    config = get_openai_config()
    client = create_openai_client(config)
    functions = load_function_schemas()
    functions_module = load_functions_module()

    messages = [{"role": "system", "content": ""}]

    # Start keyboard monitoring
    start_keyboard_monitor()
    
    try:
        while True:
            todo_md = get_todo_md()
            numbered_todo = format_numbered_todo(todo_md)
            system_prompt_filled = fill_system_prompt(system_prompt_template, numbered_todo)

            # Show current status
            status_indicator = "🎤 LISTENING" if listening_enabled else "⌨️  TEXT INPUT"
            print(f"\n[{status_indicator}] Ready for input...")
            print("Press Cmd+Option+Shift to toggle voice listening, Cmd+Ctrl+Alt for new markdown file")
            
            # Use the enhanced user input function that supports voice
            user_input = get_user_input_with_voice()
            if not user_input.strip() or any(user_input.lower().startswith(x) for x in [
                "quit",
                "exit",
                "stop",
            ]):
                logger.info("Exiting application...")
                break

            user_prompt_filled = fill_user_prompt(user_prompt_template, user_input)

            messages[0] = {"role": "system", "content": system_prompt_filled}
            messages.append({"role": "user", "content": user_prompt_filled})

            logger.debug(f"Full messages list before LLM call: {messages}")
            response_message = get_model_response(client, messages, functions)
            logger.debug(f"LLM response: {response_message}")

            while has_function_call(response_message):
                function_name, function_args = get_function_details(response_message)
                function_result = execute_function_call(
                    functions_module, function_name, function_args, todo_md.splitlines()
                )

                todo_md = get_todo_md()

                git_diff_result = get_git_diff()
                if git_diff_result:
                    function_result += f"\n\nChanges made:\n{git_diff_result}"

                messages = add_function_call_to_messages(
                    messages, response_message, function_name, function_result
                )

                logger.debug(f"Full messages list before LLM call: {messages}")
                response_message = get_model_response(client, messages, functions)
                logger.debug(f"LLM response: {response_message}")

            change_message = get_clean_git_diff()
            if change_message:
                logger.info(change_message)
                commit_todo_changes(user_input)

            display_model_response_with_tts(client, response_message)
            messages.append({"role": "assistant", "content": response_message.content})
    
    finally:
        # Ensure keyboard monitoring is stopped when the app exits
        stop_keyboard_monitor()


if __name__ == "__main__":
    app()
