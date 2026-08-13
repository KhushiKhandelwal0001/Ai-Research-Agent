"""
AI Research Agent
------------------
Takes a question, searches the web, and gives a researched answer.
"""

import os
import json
from dotenv import load_dotenv
from openai import OpenAI
from duckduckgo_search import DDGS

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("No OPENAI_API_KEY found. Check your .env file.")

client = OpenAI(api_key=api_key)


def search_web(query, max_results=3):
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=max_results))
        if not results:
            return "No results found."
        return "\n\n".join(
            f"Title: {r.get('title')}\nSnippet: {r.get('body')}\nURL: {r.get('href')}"
            for r in results
        )
    except Exception as e:
        return f"Search failed: {e}"


tools = [
    {
        "type": "function",
        "function": {
            "name": "search_web",
            "description": "Search the web for current information on a topic",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "The search query"}
                },
                "required": ["query"],
            },
        },
    }
]


def run_agent(user_question, max_steps=5):
    messages = [
        {
            "role": "system",
            "content": (
                "You are a research assistant. Use the search_web tool to find "
                "current, accurate information before answering. Cite sources "
                "by URL. When you have enough information, give a clear, "
                "structured final answer."
            ),
        },
        {"role": "user", "content": user_question},
    ]

    for step in range(max_steps):
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            tools=tools,
        )
        msg = response.choices[0].message
        messages.append(msg.model_dump())

        if msg.tool_calls:
            for call in msg.tool_calls:
                args = json.loads(call.function.arguments)
                print(f"\n[Searching]: {args['query']}")
                result = search_web(args["query"])
                messages.append(
                    {"role": "tool", "tool_call_id": call.id, "content": result}
                )
        else:
            print("\n===== ANSWER =====\n")
            print(msg.content)
            return

    print("\n[Stopped: reached max steps]")


if __name__ == "__main__":
    question = input("What would you like me to research? ")
    run_agent(question)