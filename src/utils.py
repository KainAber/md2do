import yaml
import json
import logging
import subprocess
import re
import importlib
import os
from pathlib import Path
from openai import OpenAI

debug_level = logging.DEBUG if os.getenv('DEBUG') else logging.INFO
logging.basicConfig(
    level=debug_level,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

logger.debug("Debug mode enabled - showing detailed logs")

logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("openai").setLevel(logging.WARNING)

def get_system_prompt():
    file_path = Path(__file__).parent.parent / "prompts" / "system_prompt_template.txt"
    with open(file_path, "r") as f:
        return f.read()

def get_user_prompt():
    file_path = Path(__file__).parent.parent / "prompts" / "user_prompt_template.txt"
    with open(file_path, "r") as f:
        return f.read()

def get_openai_config():
    file_path = Path(__file__).parent.parent / "openai_api_config.yml"
    with open(file_path, "r") as f:
        return yaml.safe_load(f)

def create_openai_client(config):
    return OpenAI(api_key=config["api key"])

def load_function_schemas():
    file_path = Path(__file__).parent / "functions.json"
    with open(file_path, "r") as f:
        return json.load(f)

def load_functions_module():
    return importlib.import_module("src.functions")

def get_todo_md():
    file_path = Path(__file__).parent.parent / "todo.md"
    with open(file_path, "r") as f:
        return f.read()

def format_numbered_todo(todo_content):
    lines = todo_content.splitlines()
    return "\n".join(f"{i+1}: {line}" for i, line in enumerate(lines))

def fill_system_prompt(system_prompt_template, numbered_todo):
    return system_prompt_template.format(numbered_todo=numbered_todo)

def fill_user_prompt(user_prompt_template, user_input):
    return user_prompt_template.format(user_input=user_input)

def get_user_input():
    return input("> ").strip()

def get_model_response(client, messages, functions):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        functions=functions,
        function_call="auto",
        temperature=0.0,
        top_p=1.0,
        max_tokens=512
    )
    return response.choices[0].message

def has_function_call(response_message):
    return hasattr(response_message, 'function_call') and response_message.function_call is not None

def get_function_details(response_message):
    function_name = response_message.function_call.name
    function_args = json.loads(response_message.function_call.arguments)
    return function_name, function_args

def execute_function_call(functions_module, function_name, arguments, todo_lines):
    try:
        func = getattr(functions_module, function_name)
        result = func(todo_lines, **arguments)
        return result
        
    except AttributeError:
        return f"ERROR: Unknown function: {function_name}"
    except Exception as e:
        return f"ERROR: Error executing {function_name}: {str(e)}"

def get_git_diff():
    file_path = Path(__file__).parent.parent / "todo.md"
    diff_output = None
    try:
        result = subprocess.run(["git", "diff", "-U1", "--word-diff=color", str(file_path)], 
                              capture_output=True, text=True, check=True)
        
        if result.stdout.strip():
            diff_output = result.stdout
        
    except subprocess.CalledProcessError as e:
        logger.error(f"Git diff failed: {e}")
    
    return diff_output

def get_clean_git_diff():
    file_path = Path(__file__).parent.parent / "todo.md"
    try:
        result = subprocess.run(["git", "diff", "-U1", "--word-diff=color", str(file_path)], 
                              capture_output=True, text=True, check=True)
        print(result.stdout)
        if not result.stdout.strip():
            return ""
        lines = result.stdout.split('\n')
        clean_lines = []
        for line in lines:
            clean_line = re.sub(r'\x1b\[[0-9;]*[mK]', '', line)
            bad_line_starts = ['diff --git', 'index', '---', '+++', '@@']
            print(clean_line)
            if (any(clean_line.startswith(x) for x in bad_line_starts)):
                clean_lines.append('')
            else:
                clean_lines.append(line)
        content = '\n'.join(clean_lines)
        content = re.sub(r'\n\s*\n\s*\n+', '\n\n', content)
        content = content.strip('\n')
        if content:
            return f"Changes:\n{content}"
        else:
            return ""
    except subprocess.CalledProcessError as e:
        logger.error(f"Git diff failed: {e}")
        return ""

def commit_todo_changes(user_input):
    file_path = Path(__file__).parent.parent / "todo.md"
    try:
        subprocess.run(["git", "add", str(file_path)], capture_output=True, check=True)
        subprocess.run(["git", "commit", "-m", f"Update todo: {user_input}"], capture_output=True, check=True)
    except subprocess.CalledProcessError as e:
        logger.error(f"Git commit failed: {e}")

def add_function_call_to_messages(messages, response_message, function_name, function_result):
    new_messages = messages + [
        response_message,
        {
            "role": "function",
            "name": function_name,
            "content": function_result
        }
    ]
    return new_messages

def display_model_response(response_message):
    logger.info(response_message.content)

 