# Streamlit + Ollama Chat (qwen2:7b)

A simple Streamlit chat UI to talk to a local Ollama model (default `qwen2:7b`).

## Features
- Streamed responses from Ollama
- Sidebar to set model name, temperature, and system prompt
- Persistent session chat history

## Requirements
- Ollama installed and running locally (Windows: start the Ollama app or run `ollama serve`)
- Python 3.9+
- Packages in `requirements.txt`

## Quick start

1. Install dependencies:

```powershell
pip install -r requirements.txt
```

2. Make sure your model is available (example):

```powershell
ollama pull qwen2:7b
```

3. Run the app:

```powershell
streamlit run app.py
```

4. Open the provided local URL in your browser.

## Notes
- Change the default model via env var `OLLAMA_MODEL` or in the sidebar.
- If you see a connection warning, ensure Ollama is running at http://127.0.0.1:11434.
- You can set a custom system prompt to steer the assistant.
