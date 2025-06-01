# 🧠 AI Coding Agent (Terminal-Based)

This is a terminal-based AI Coding Agent that uses OpenAI's API to interactively build full-stack applications, particularly focused on creating and modifying ReactJS projects. It understands context, runs shell commands, writes to files, installs dependencies, and even launches projects in the browser — all from a single CLI interface.

---

## 🚀 Features

- 📁 Automatically generate React project structures
- 🧠 Plan → Act → Observe architecture using OpenAI's assistant
- ✍️ Modify project files (e.g., add login pages, update components)
- 📦 Run `npm install`, `npm start`, etc. from within the agent
- 🌐 Opens project in Chrome (cross-platform)
- 🔄 Supports follow-up prompts and iterative development

---

## 🛠️ Tools Used

- **Python 3.11**
- **OpenAI API**
- **dotenv** for API key management
- **requests** for basic HTTP functionality
- **subprocess/os** for command execution
- **platform/webbrowser** for opening URLs across OSes
