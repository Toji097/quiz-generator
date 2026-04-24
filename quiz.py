import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def quiz(questions):
    prompt = f"""
    Analyse the subject being asked about to make questions on.
    Return exactly this format:
    Subject: [The subject being asked about]
    Questions: [Provide 3 questions in the range of Easy/Medium/Hard]

    Text: {questions}
    """

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{
            "role": "user",
            "content": prompt
        }]
    )

    return response.choices[0].message.content

print("Quiz generator - type 'quit' to exit\n")

while True:
    user_input = input("Enter Subject to make questions on: ")
    if user_input.lower() == "quit":
        break
    result = quiz(user_input)
    print(f"\n{result}\n")



