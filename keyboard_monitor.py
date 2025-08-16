#!/usr/bin/env python3
import yaml
import subprocess
from datetime import datetime
from pynput import keyboard
import os

keys = set()

def new_md():
    timestamp = datetime.now().strftime("%Y-%m-%d--%H-%M-%S")
    filename = f"{timestamp}.md"
    subprocess.run(["open", "-a", "Terminal", os.path.expanduser("~")], capture_output=True)
    subprocess.run(["osascript", "-e", f'tell application "Terminal" to do script "nvimtmp {filename}" in front window'], capture_output=True)

def on_press(key):
    key_str = key.name if hasattr(key, 'name') else str(key)
    keys.add(key_str)
    check()

def on_release(key):
    key_str = key.name if hasattr(key, 'name') else str(key)
    keys.discard(key_str)

def check():
    with open("keyboard_shortcuts.yaml", "r") as f:
        config = yaml.safe_load(f)
    
    for shortcut in config["shortcuts"].values():
        if set(shortcut["keys"]).issubset(keys):
            exec(shortcut["function"])
            keys.clear()
            break

if __name__ == "__main__":
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()
