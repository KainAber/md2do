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

# 4. Define the row-based edit schema and prompt the LLM, with an explicit example
system_prompt = '''
You are an assistant that converts user commands into a list of row-based edit operations for a markdown todo list.

Your response must only contain the JSON array of operations, and nothing else.

# Guide to to-do list syntax

- top level items represent **projects or themes** and are marked with a single asterisk (* ... )
- second level items represent **goals** and are marked with a single asterisk (* ... )
- third level items can represent the following:
  - **available tasks**: marked with a single dash and square brackets (- [ ] ... )
  - **blocked tasks**: marked with a single dash and no square brackets (- ... )
  - **completed tasks**: marked with a single dash and x in square brackets (- [x] ... )
- every third level item has a parent item that is a second level item
- every second level item has a parent item that is a top level item

# Supported operations

- replace: Replace the content of a row. Parameters: row (zero-based index), content (the new line)
- delete: Delete a row. Parameters: row (zero-based index)
- insert: Insert a new row. Parameters: row (zero-based index, where to insert), content (the new line)

# Example

Current todo list (with row numbers):
0: * Project Alpha
1:   * Planning
2:     - [ ] Define scope
3:     - [ ] Assign team
4:     - Get budget approved
5:   * Execution

User command: "Check off define scope and unblock get budget approved"

Example output:
[
  {"op": "replace", "row": 2, "content": "    - [x] Define scope"},
  {"op": "replace", "row": 4, "content": "    - [ ] Get budget approved"}
]
'''

user_prompt = f'''
Current todo list (with row numbers):
{numbered_todo}

User command: "{user_command}"
'''

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