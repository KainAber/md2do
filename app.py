import yaml
import json
from openai import OpenAI

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
    for op in others:
        idx = op["row"] - 1
        if op["op"] == "replace":
            lines[idx] = op["content"]
        elif op["op"] == "insert":
            lines.insert(idx, op["content"])
    for op in sorted(deletes, key=lambda x: -x["row"]):
        idx = op["row"] - 1
        del lines[idx]
    return lines

print("Type your todo command (or 'exit' to quit):")
while True:
    user_command = input("> ").strip()
    if user_command.lower() in ("exit", "quit"):
        print("Exiting.")
        break
    # Read current todo.md
    with open("todo.md", "r") as f:
        todo_lines = f.read().splitlines()
    numbered_todo = "\n".join(f"{i+1}: {line}" for i, line in enumerate(todo_lines))
    user_prompt = user_prompt_template.format(numbered_todo=numbered_todo, user_command=user_command)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.0,
        top_p=1.0,
        max_tokens=512
    )
    content = response.choices[0].message.content
    print("Raw LLM output:", content)
    try:
        operations = json.loads(content)
    except Exception as e:
        print("Failed to parse LLM output as JSON:", content)
        continue
    new_todo_lines = apply_row_operations(todo_lines, operations)
    with open("todo.md", "w") as f:
        f.write("\n".join(new_todo_lines))
    print("todo.md updated!\n") 