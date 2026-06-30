from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq()

while True:
    user_input = input("Bạn: ")

    if user_input.lower() in ["exit", "quit"]:
        print("Thoát.")
        break

    completion = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {
                "role": "user",
                "content": user_input
            }
        ],
        stream=True
    )

    print("Bot: ", end="")

    for chunk in completion:
        print(chunk.choices[0].delta.content or "", end="")

    print("\n")