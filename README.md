# AI Research Agent

A simple AI agent that searches the web and answers research questions,
built with the OpenAI API and DuckDuckGo search.

## Setup

1. Create a virtual environment: `python -m venv venv`
2. Activate it: `venv\Scripts\activate` (Windows)
3. Install dependencies: `pip install -r requirements.txt`
4. Create a `.env` file with your OpenAI key: `OPENAI_API_KEY=your_key_here`
5. Run: `python agent.py`

## How it works

The agent uses a reasoning loop: it decides whether it needs to search the
web, calls the search tool if so, reads the results, and repeats until it
has enough information to give a final answer.