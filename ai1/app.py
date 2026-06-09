import os
import google.generativeai as genai
from dotenv import load_dotenv


def read_file(filename):
  try:
    with open(filename,"r",encoding="utf-8") as f:
      return f.read()
  except Exception as e:
        return str(e)


load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-2.5-flash")

system_prompt = """
You are an assistant.
Id you need to read a file, respond ONLY in this format:
TOOL: read_file(filename)
Do not explain anything else.
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

    if reply.startswith("TOOL: read_file("):
        filename = reply[len("TOOL: read_file("):-1]
        content = read_file(filename)

        print("Tool Result:")
        print(content)
        continue

    print("AI:", reply, "\n")

    chat_history.append(f"AI: {reply}")
