import os
from typing import List, Dict, Any

import streamlit as st
import ollama


st.set_page_config(page_title="Ollama Chat (Streamlit)", page_icon="💬", layout="centered")

DEFAULT_MODEL = os.getenv("OLLAMA_MODEL", "qwen2:7b")
DEFAULT_SYSTEM_PROMPT = os.getenv("SYSTEM_PROMPT", "You are a helpful AI assistant.")

if "messages" not in st.session_state:
	# {"role": "user"|"assistant"|"system", "content": str}
	st.session_state.messages = []

if "connected" not in st.session_state:
	st.session_state.connected = False


def check_ollama_connection() -> bool:
	try:
		_ = ollama.list()
		return True
	except Exception:
		return False


def ensure_system_message(system_prompt: str) -> List[Dict[str, str]]:
	msgs = []
	if system_prompt.strip():
		msgs.append({"role": "system", "content": system_prompt.strip()})
	msgs.extend(st.session_state.messages)
	return msgs


def stream_chat_completion(model: str, messages: List[Dict[str, str]], temperature: float = 0.7):
	for chunk in ollama.chat(
		model=model,
		messages=messages,
		stream=True,
		options={"temperature": temperature},
	):
		# { 'model': ..., 'message': { 'role': 'assistant', 'content': '...' } }
		msg = chunk.get("message", {})
		content = msg.get("content", "")
		if content:
			yield content


with st.sidebar:
	st.title("⚙️ Settings")
	model_name = st.text_input("Model", value=DEFAULT_MODEL, help="Name of your local Ollama model")
	temperature = st.slider("Temperature", 0.0, 1.0, 0.7, 0.05)
	system_prompt = st.text_area("System Prompt", value=DEFAULT_SYSTEM_PROMPT, height=100)

	col1, col2 = st.columns(2)
	with col1:
		if st.button("Clear Chat", use_container_width=True):
			st.session_state.messages = []
			st.rerun()
	with col2:
		connected = check_ollama_connection()
		st.session_state.connected = connected
		st.markdown(
			f"Server: {'🟢 Connected' if connected else '🔴 Not reachable'}",
			help="Checks connection to the local Ollama server (http://127.0.0.1:11434)",
		)

st.title("💬 Chat with Ollama")
st.caption("Local model via Ollama + Streamlit")

if not st.session_state.connected:
	st.warning(
		"Ollama server not reachable.\n\n"
	)

for m in st.session_state.messages:
	if m["role"] == "user":
		with st.chat_message("user"):
			st.markdown(m["content"])
	elif m["role"] == "assistant":
		with st.chat_message("assistant"):
			st.markdown(m["content"])

user_input = st.chat_input("Type your message and press Enter...")

if user_input:
	st.session_state.messages.append({"role": "user", "content": user_input})

	with st.chat_message("user"):
		st.markdown(user_input)

	with st.chat_message("assistant"):
		placeholder = st.empty()
		full_response = ""

		try:
			msgs_with_system = ensure_system_message(system_prompt)
			for chunk in stream_chat_completion(model_name, msgs_with_system, temperature):
				full_response += chunk
				placeholder.markdown(full_response)
		except Exception as e:
			full_response = f"Error: {e}"
			placeholder.error(full_response)

	st.session_state.messages.append({"role": "assistant", "content": full_response})
