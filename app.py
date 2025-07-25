import yaml
import json
from openai import OpenAI

# Debug mode - set to True to see LLM output and user input
DEBUG_MODE = False

# Load prompts and config once
with open("system_prompt.txt", "r") as f:
    system_prompt = f.read()
with open("user_prompt_template.txt", "r") as f:
    user_prompt_template = f.read()
with open("openai_api_config.yml", "r") as f:
    config = yaml.safe_load(f)

client = OpenAI(api_key=config["api key"])

def apply_row_operations(lines, operations):
    deletes = [op for op in operations if op["op"] == "delete"]
    others = [op for op in operations if op["op"] != "delete"]
    # Separate moves to apply after others (to avoid index confusion)
    moves = [op for op in others if op["op"] == "move"]
    non_moves = [op for op in others if op["op"] != "move"]
    for op in non_moves:
        idx = op["row"] - 1
        if op["op"] == "replace":
            lines[idx] = op["content"]
        elif op["op"] == "insert":
            lines.insert(idx, op["content"])
    for op in sorted(deletes, key=lambda x: -x["row"]):
        idx = op["row"] - 1
        del lines[idx]
    # Apply moves after all other ops
    for op in moves:
        from_idx = op["row"] - 1
        to_idx = op["to"] - 1
        line = lines.pop(from_idx)
        # If moving down, insertion index decreases by 1 after pop
        if to_idx > from_idx:
            to_idx -= 1
        lines.insert(to_idx, line)
    return lines

messages = []

print("Type your todo command (or 'exit' to quit):")
while True:
    user_command = input("> ").strip()
    if user_command.lower() in ("exit", "quit"):
        print("Exiting.")
        break
    
    if DEBUG_MODE:
        print(f"\n[DEBUG] User input: {user_command}")
    
    # Read current todo.md
    with open("todo.md", "r") as f:
        todo_lines = f.read().splitlines()
    numbered_todo = "\n".join(f"{i+1}: {line}" for i, line in enumerate(todo_lines))
    # Prepare system prompt with current todo.md
    system_prompt_with_todo = system_prompt.format(numbered_todo=numbered_todo)
    # Build new messages list: system prompt, then all previous user/assistant messages, then new user message
    new_messages = [
        {"role": "system", "content": system_prompt_with_todo},
    ]
    if messages:
        new_messages.extend(messages[1:])  # skip previous system prompt
    new_messages.append({"role": "user", "content": user_command})
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=new_messages,
        temperature=0.0,
        top_p=1.0,
        max_tokens=512
    )
    content = response.choices[0].message.content
    if DEBUG_MODE:
        print(f"[DEBUG] LLM output:\n{content}")
    # Parse for JSON array and helpful comment
    operations = None
    comment = None
    
    lines = content.split('\n')
    stripped_lines = [line.strip() for line in lines]
    
    try:
        start_idx = stripped_lines.index('[')
        end_idx = stripped_lines.index(']', start_idx) + 1
        
        json_str = '\n'.join(lines[start_idx:end_idx])
        operations = json.loads(json_str)
        comment = '\n'.join(lines[end_idx:]).strip()
        
        new_todo_lines = apply_row_operations(todo_lines, operations)
        with open("todo.md", "w") as f:
            f.write("\n".join(new_todo_lines))
        print(comment + "\n")
    except ValueError:
        print("[Error] Could not find JSON array in LLM output.\n")
        continue
    except Exception as e:
        print(f"[Error] Failed to parse operations as JSON: {e}\nRaw operations string:\n{json_str}\n")
        continue
    # Update messages for next turn (keep system prompt out, add user and assistant)
    messages = new_messages
    messages.append({"role": "assistant", "content": content}) 