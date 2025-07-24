import speech_recognition as sr
import ollama

recognizer = sr.Recognizer()
with sr.Microphone() as source:
    print("Please say your todo update command...")
    audio = recognizer.listen(source)
    command = recognizer.recognize_google(audio)
    print(f"You said: {command}")

with open("todo.md", "r") as f:
    todo_content = f.read()

system_prompt = (
    "You are a helpful assistant for editing markdown todo lists. "
    "You will be given a to-do list in markdown format together with an instruction to update the to-do list. "
    "Your output should consist only of the updated markdown text **without any other text or comments**."
)

prompt = (
    "**INSTRUCTION**\n\n" + command + "\n\n\n"
    "**TO-DO LIST** (only return what is below this line)\n\n" + todo_content
)

response = ollama.chat(
    model="mistral",
    messages=[
        {"role": "system", "content": "You are a helpful assistant for editing markdown todo lists."},
        {"role": "user", "content": prompt}
    ]
)

result = response["message"]["content"]

with open("todo.md", "w") as f:
    f.write(result)

print("todo.md updated!") 