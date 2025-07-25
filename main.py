from openai import OpenAI
import yaml
import json

# 1. Get user command (dummy text input for now)
user_command = "Unblock implement fix"

# 2. Read current todo.md
with open("todo.md", "r") as f:
    todo_lines = f.read().splitlines()

# 3. Prepare the todo list with row numbers for the prompt
numbered_todo = "\n".join(f"{i}: {line}" for i, line in enumerate(todo_lines))

# 4. Load prompts from external files
with open("system_prompt.txt", "r") as f:
    system_prompt = f.read()
with open("user_prompt_template.txt", "r") as f:
    user_prompt_template = f.read()
user_prompt = user_prompt_template.format(numbered_todo=numbered_todo, user_command=user_command)

# Load OpenAI API key from YAML
with open("openai_api_config.yml", "r") as f:
    config = yaml.safe_load(f)

client = OpenAI(api_key=config["api key"])

# Call OpenAI ChatCompletion (new API)
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ],
    temperature=0.0,
    max_tokens=512
)

# 4b. Log the raw JSON output from the LLM
content = response.choices[0].message.content
print("Raw LLM output:", content)

# 5. Parse the LLM's JSON output
try:
    operations = json.loads(content)
except Exception as e:
    print("Failed to parse LLM output as JSON:", content)
    exit(1)

# 6. Apply the operations to the markdown lines
def apply_row_operations(lines, operations):
    # To avoid messing up indices, process deletes in reverse order, others in order
    deletes = [op for op in operations if op["op"] == "delete"]
    others = [op for op in operations if op["op"] != "delete"]
    # Apply non-delete operations
    for op in others:
        if op["op"] == "replace":
            lines[op["row"]] = op["content"]
        elif op["op"] == "insert":
            lines.insert(op["row"], op["content"])
    # Apply deletes in reverse order
    for op in sorted(deletes, key=lambda x: -x["row"]):
        del lines[op["row"]]
    return lines

new_todo_lines = apply_row_operations(todo_lines, operations)

# 7. Overwrite todo.md with the updated content
with open("todo.md", "w") as f:
    f.write("\n".join(new_todo_lines))

print("todo.md updated!") 