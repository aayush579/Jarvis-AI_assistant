# Jarvis-AI (Full Build: Console + Plugins + Memory + GUI scaffold)

## Quickstart
1) Create a Python venv (recommended) and install deps:
```bash
pip install -r requirements.txt
```
2) Add your API keys in `config.json`.
3) Run (console):
```bash
python jarvis.py
```
4) (Optional GUI) Inside `gui/`:
```bash
npm install
npm start
```

## API Keys (edit `config.json`)
- `OPENAI_API_KEY` → for GPT responses
- `WEATHER_API_KEY` → from OpenWeatherMap
- `NEWS_API_KEY` → from NewsAPI
- `GOOGLE_CLIENT_ID` / `GOOGLE_CLIENT_SECRET` → for Google Calendar OAuth

## Packaging as .exe (Windows)
```bash
pip install pyinstaller
pyinstaller --onefile --noconsole jarvis.py
```
Output is in `dist/`.


# 🤖 Jarvis AI — Intelligent Personal Assistant

Jarvis AI is a **modular, AI-powered personal assistant** designed to automate daily tasks, assist developers, and demonstrate practical applications of **AI reasoning, system automation, and scalable software architecture**.

Unlike basic chatbots, Jarvis AI functions as an **intelligent agent** capable of understanding natural language, maintaining persistent memory, executing multi-step tasks, and integrating with system-level tools.

---

## 🎯 Problem Statement

Most existing personal assistants:
- Rely on predefined commands
- Lack long-term memory and contextual awareness
- Are difficult to extend or customize
- Cannot autonomously execute chained tasks

This project addresses these limitations by implementing a **production-style assistant architecture** focused on **extensibility, autonomy, and real-world usability**.

---

## 💡 Solution Overview

Jarvis AI combines:
- Natural language understanding
- Persistent memory
- Voice interaction
- Plugin-based extensibility
- Desktop GUI
- Autonomous agent workflows

The system is designed so that **new features can be added without modifying core logic**, following clean software engineering principles.

---

## ✨ Core Features

- 🎙️ **Voice Interaction**
  - Wake-word activation
  - Speech-to-text and text-to-speech

- 🧠 **AI Reasoning Engine**
  - Context-aware responses
  - Multi-step task planning

- ⏰ **Reminder & Scheduling System**
  - Natural language time parsing
  - Persistent notifications

- 🗂️ **Personal Memory Module**
  - Stores user preferences and history
  - Improves responses over time

- 🧩 **Plugin-Based Architecture**
  - Feature isolation
  - Easy extensibility

- 🖥️ **Desktop GUI**
  - Electron + React interface
  - Clean, developer-focused UI

- 🤖 **Autonomous Agent Mode**
  - Executes tasks independently
  - Handles chained commands

- 🔌 **System & Tool Automation**
  - File operations
  - Application control
  - Optional integrations (Calendar, Notion)

---

## 🏗️ Architecture & Design

