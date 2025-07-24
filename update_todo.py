import speech_recognition as sr
from transformers import pipeline

recognizer = sr.Recognizer()
with sr.Microphone() as source:
    print("Please say your todo update command...")
    audio = recognizer.listen(source)
    command = recognizer.recognize_google(audio)
    print(f"You said: {command}")

with open("todo.md", "r") as f:
    todo_content = f.read()

generator = pipeline("text-generation", model="distilgpt2")
prompt = (
    "You are a helpful assistant for editing markdown todo lists. "
    "Here is the current todo.md file:\n" + todo_content +
    "\n\nUser command: '" + command + "'\n"
    "Update the todo.md file accordingly. Output only the new todo.md content."
)

result = generator(prompt, max_length=512, num_return_sequences=1)[0]['generated_text']

with open("todo.md", "w") as f:
    f.write(result)

print("todo.md updated!") 