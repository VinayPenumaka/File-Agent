import os
import json
import google.generativeai as genai
from dotenv import load_dotenv


# tools
def read_file(filename):
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return str(e)


def list_files():
    return os.listdir()


def write_file(filename, content):
    try:
        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)
        return "File written successfully"
    except Exception as e:
        return str(e)


def search_web(query):
    return f"(Mock) Search results for: {query}"


# memory
# def save_memory(history):
#     with open("memory.json", "w") as f:
#         json.dump(history, f)

# def load_memory():
#     try:
#         with open("memory.json") as f:
#             return json.load(f)
#     except:
#         return []


def clean_json(reply):
    reply = reply.strip()

    if reply.startswith("```"):
        parts = reply.split("```")
        reply = parts[1]
        if reply.strip().startswith("json"):
            reply = reply.strip()[4:]

    return reply.strip()


load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-2.5-flash")

system_prompt = """
You are an AI agent.

You can think step-by-step and use tools.

RULES:
- If you want to use a tool, respond ONLY in JSON
- Do NOT use markdown

Format:
{
  "thought": "your reasoning",
  "tool": "tool_name",
  "args": {}
}

- If no tool is needed, respond normally

Available tools:
- read_file(filename)
- list_files()
- write_file(filename, content)
- search_web(query)
"""


MAX_TOOL_OUTPUT = 300
MAX_STEPS = 3

# chat_history = load_memory()
chat_history = []


while True:
    user_input = input("You: ")

    if user_input.lower() == "exit":
        # save_memory(chat_history)
        break

    for step in range(MAX_STEPS):

        prompt = system_prompt + "\nUser: " + user_input

        response = model.generate_content(prompt)
        reply = response.text

        try:
            cleaned = clean_json(reply)
            data = json.loads(cleaned)

            thought = data.get("thought", "")
            tool = data.get("tool")
            args = data.get("args", {})

            print(f"🧠 Thought: {thought}")

            if tool == "read_file":
                result = read_file(args.get("filename", ""))
            elif tool == "list_files":
                result = list_files()
            elif tool == "write_file":
                result = write_file(
                    args.get("filename", ""),
                    args.get("content", "")
                )
            elif tool == "search_web":
                result = search_web(args.get("query", ""))
            else:
                result = "Unknown tool"

            short_result = str(result)[:MAX_TOOL_OUTPUT]

            print("🔧 Tool Result:\n", short_result)

            user_input = f"Tool result: {short_result}"

        except Exception:
            print("AI:", reply, "\n")
            break

