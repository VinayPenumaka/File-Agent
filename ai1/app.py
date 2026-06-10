import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

def read_file(filename):
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return str(e)

def list_files():
    return os.listdir()

def write_file(filename, content):
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
    return "File written successfully"


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
You are an assistant.

If you use a tool:
- Respond with ONLY raw JSON
- Do NOT use ``` blocks

Example:
{
  "tool": "read_file",
  "args": {"filename": "notes.txt"}
}

Available tools:
- read_file(filename)
- list_files()
- write_file(filename, content)
"""

chat_history = []

while True:
    user_input = input("You: ")

    if user_input.lower() == "exit":
        break

    chat_history.append(f"You: {user_input}")

    prompt = system_prompt + "\n" + "\n".join(chat_history)

    response = model.generate_content(prompt)
    reply = response.text

    try:
        cleaned = clean_json(reply)
        data = json.loads(cleaned)

        tool = data.get("tool")

        if tool == "read_file":
            result = read_file(data["args"]["filename"])

        elif tool == "list_files":
            result = list_files()

        elif tool == "write_file":
            result = write_file(
                data["args"]["filename"],
                data["args"]["content"]
            )

        else:
            result = "Unknown tool"

        print("Tool Result:\n", result)

        # ✅ IMPORTANT: give result back to agent
        chat_history.append(f"Tool result: {result}")
        continue

    except Exception:
        pass

    print("AI:", reply, "\n")
    chat_history.append(f"AI: {reply}")