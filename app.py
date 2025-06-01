from dotenv import load_dotenv
from openai import OpenAI
from datetime import datetime
import requests
import json
import os
import platform
import webbrowser

load_dotenv()

client = OpenAI()

import subprocess

def run_command(cmd: str, background: bool = False):
    if background:
        subprocess.Popen(cmd, shell=True)
        return f"Started command in background: {cmd}"
    else:
        return os.system(cmd)

def run_command_bg(cmd: str):
    return run_command(cmd, background=True)

def create_react_project(project_name):
    return run_command(f"npx create-react-app {project_name.lower() if project_name[0].isupper() else project_name}")

def write_to_file(file_path, content):
    with open(file_path, "w") as f:
        f.write(content)
    return f"{file_path} updated successfully."

def append_to_file(file_path, content):
    with open(file_path, "a") as f:
        f.write(content)
    return f"{file_path} appended successfully."

def read_file(file_path):
    with open(file_path, "r") as f:
        return f.read()

def open_in_chrome(url):
    system = platform.system()
    if system == "Macp":  # macOS
        os.system(f'open -a "Google Chrome" {url}')
    elif system == "Windows":
        os.system(f'start chrome {url}')
    elif system == "Linux":
        os.system(f'google-chrome {url} || chromium-browser {url} || xdg-open {url}')
    else:
        webbrowser.open(url)
    return f"Opened {url} in Chrome"

available_tools = {
    "run_command": run_command,
    "run_command_bg": run_command_bg,
    "create_react_project": create_react_project,
    "write_to_file": write_to_file,
    "append_to_file": append_to_file,
    "read_file": read_file,
    "open_in_chrome": open_in_chrome,
}

SYSTEM_PROMPT = """
    You are a helpfull AI assistant who is specialized in resolving user query.
    You work on start, plan, action, observe mode.

    For the given user query and available tools, plan the step by step execution, based on the planning, select the relevant tool from the available tools, and based on the tool selection you perform an action to call the tool.

    Wait for the observation and based on the observation from the tool call resolve the user query.

    Rules:
    - Follow the Output JSON Format.
    - Always perform one step at a time and wait for tnext input.
    - Carefully analyse the user query

    Output JSON Format:
    {{
        "step": "string",
        "content": "string",
        "function": "The name of function if the step is action",
        "input": "The input parameter for the function",
    }}

    Available Tools:
    - "run_command": Takes a linux command as a string and executes the command and returns the iutput after executing it.
    - "run_command_bg": Takes a linux command as a string and executes the command in background.
    - "create_react_project": Takes a project name and initializes a React project.
    - "write_to_file": Takes a file path and content, writes content into the file.
    - "append_to_file": Takes a file path and content, appends content.
    - "read_file": Reads and returns content of the file.
    - "open_in_chrome": Takes a URL and opens it in Google Chrome browser.

    Example:
    User Query: "Create a TODO app in React"
    Output: {"step": "plan", "content": "User wants to create a new React app named TodoApp"}
    Output: {"step": "action", "function": "create_react_project", "input": "TodoApp"}
    Output: {"step": "observe", "output": "React app created successfully"}
    Output: {"step": "plan", "content": "Now, the App.js file should be updated to support TODO functionality"}
    Output: {"step": "action", "function": "write_to_file", "input": {
        "file_path": "TodoApp/src/App.js",
        "content": "import React, { useState } from 'react';\n\nfunction App() {\n  const [todos, setTodos] = useState([]);\n  const [input, setInput] = useState('');\n\n  const addTodo = () => {\n    if (input.trim()) {\n      setTodos([...todos, input]);\n      setInput('');\n    }\n  };\n\n  return (\n    <div>\n      <h1>TODO App</h1>\n      <input value={input} onChange={(e) => setInput(e.target.value)} />\n      <button onClick={addTodo}>Add</button>\n      <ul>\n        {todos.map((todo, index) => <li key={index}>{todo}</li>)}\n      </ul>\n    </div>\n  );\n}\n\nexport default App;"
    }}
    Output: {"step": "observe", "output": "App.js updated successfully"}
    Output: {"step": "plan", "content": "Now install dependencies and run the app"}
    Output: {"step": "action", "function": "run_command", "input": "cd TodoApp && npm install"}
    Output: {"step": "observe", "output": "Dependencies installed"}
    Output: {"step": "action", "function": "run_command_bg", "input": "cd TodoApp && npm start"}
    Output: {"step": "action", "function": "open_in_chrome", "input": "http://localhost:3000"}
    Output: {"step": "output", "content": "Your TODO app is ready and running at http://localhost:3000"}
"""

messages=[
    {"role": "system", "content": SYSTEM_PROMPT}, 
]

while True:
    query = input(">")
    messages.append({"role": "user", "content": query})

    while True:
        response = client.chat.completions.create(
            model="gpt-4.1",
            response_format={"type": "json_object"},
            messages=messages
        )

        messages.append({"role": "assistant", "content": response.choices[0].message.content})
        parsed_response = json.loads(response.choices[0].message.content)

        if parsed_response["step"] == "plan":
            print(f"Plan 🧠: {parsed_response.get('content')}")
            continue

        if parsed_response["step"] == "action":
            tool_name = parsed_response.get("function")
            tool_input = parsed_response.get("input")

            print(f"Tool 🛠️: Calling Tool: {tool_name} with input {tool_input}")

            if available_tools.get(tool_name) is not None:
                if isinstance(tool_input, dict):
                    output = available_tools[tool_name](**tool_input)
                else:
                    output = available_tools[tool_name](tool_input)
                messages.append({"role": "user", "content": json.dumps({"step": "observe", "output": output})})
                continue
        
        if parsed_response.get("step") == "output":
            print(f"🤖:", parsed_response.get("content"))
            if "running at http://localhost:3000" in parsed_response.get("content", "").lower():
                break
            break
