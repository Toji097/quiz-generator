import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def generate_questions(topic):
    prompt = f"""
    Generate exactly 3 quiz questions about {topic}. One easy, one medium, one hard.
    Return ONLY this format, nothing else:
    1. [easy question]
    2. [medium question]
    3. [hard question]
    """

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{
            "role": "user",
            "content": prompt
        }]
    ) 
    return response.choices[0].message.content

def mark_answer(question, user_answer):
    prompt = f"""
    Question: {question}
    User's answer: {user_answer}

    Is this answer correct? Be fair but strict.
    Return exactly this format:
    Result: [Correct/Incorrect]
    Correct answer: [the actual correct answer in one sentence]
    Feedback: [one sentence of feedback]
    """
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{
            "role": "user",
            "content": prompt
        }]
    )
    return response.choices[0].message.content

topic = input("Enter a topic to be quizzed on: ")
print("\nGenerating questions...\n")

questions_text = generate_questions(topic)
questions = [q.strip() for q in questions_text.strip().split('\n') if q.strip()]

score = 0

for question in questions:
    print(f"{question}")
    answer = input("Your answer: ")
    result = mark_answer(question, answer)
    print(f"\n{result}\n")
    if "Result: Correct" in result:
        score += 1

print(f"Quiz complete! You scored {score}/{len(questions)}")