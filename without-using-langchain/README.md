# ChatBot

A conversational AI assistant with:

- Tool calling for web search and code execution
- Lightweight Retrieval-Augmented Generation (RAG) memory
- Conversation summarization utilities for long chat histories
- Gradio-based chat UI for local testing

## Overview

This project prototypes a multi-tool chatbot that can answer normally, call tools when needed, and store/retrieve prior conversation context using vector similarity.

Current implementation is primarily orchestrated in `try2.ipynb`, with reusable helper modules in Python files.

## Key Capabilities

- Tool calling via OpenAI-compatible chat completions
  - `google_search`: Uses SerpAPI to fetch top search results
  - `code_n_execute`: Generates Python code with an LLM and executes it in E2B Sandbox
- RAG memory layer
  - Stores each chat turn in ChromaDB with sentence embeddings
  - Retrieves top-k relevant past messages for contextual responses
- Chat UI
  - Local `gr.ChatInterface(...)` for rapid iteration
- Summarization utilities
  - Functions to compress long histories when token usage grows

## Architecture

1. User sends a message through Gradio chat.
2. The app retrieves relevant memory snippets from ChromaDB.
3. Retrieved context is injected into the system prompt.
4. The chat model responds, optionally with tool calls.
5. Tool outputs are fed back to the model for a final answer.
6. Query/response are embedded and saved to vector memory.

## Project Structure

- `try2.ipynb`: Main prototype notebook with chat loop, tool definitions, RAG save/retrieve, and Gradio launch
- `tools.py`: External tool implementations (`google_search`, `code_n_execute`)
- `handle_tool_calls.py`: Dispatches and executes model-requested tool calls
- `summariser.py`: Conversation summarization helper utilities
- `main.py`: Additional/experimental summarization logic
- `requirements.txt`: Python dependencies

## Requirements

- Python 3.10+
- API keys and endpoint configuration in environment variables

## Environment Variables

Create a `.env` file in the project root with:

```env
NVIDIA_API_KEY=your_nvidia_key
URL=your_openai_compatible_base_url
E2B_API_KEY=your_e2b_key
SERPAPI_KEY=your_serpapi_key
```

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Running the Project

### Notebook workflow (current primary path)

1. Open `try2.ipynb`.
2. Select your Python kernel (the project virtual environment).
3. Run cells top-to-bottom.
4. Execute the final cell:

```python
gr.ChatInterface(chat).launch()
```

This starts a local Gradio chat app in your browser.

## Notes and Limitations

- The current codebase is prototype-oriented; some logic is notebook-first.
- Summarization flow is present but currently commented out in the chat loop.
- ChromaDB collection is in-process/default local client configuration.
- `requirements.txt` contains a broad set of packages; you may want to prune it for production.

## Security and Operational Guidance

- Never commit `.env` or API secrets.
- Sandbox execution is safer than local execution, but still validate prompts and outputs.
- Add strict tool-call guards and request validation before production deployment.

## Suggested Next Steps

- Move notebook orchestration into a single runnable Python entrypoint.
- Add unit tests for tool dispatch and RAG functions.
- Add persistent vector store configuration and migration strategy.
- Introduce structured logging and error monitoring.
