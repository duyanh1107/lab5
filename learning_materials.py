from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv(override = True)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)

def generate_hint_llm(question, performance, attempt):
    prompt = f"""
                You are a helpful tutor.

                Student level: {round(performance,2)}
                Attempt: {attempt}

                Question: {question}

                Give a short hint based on student level and number of attempt.
                Low level → more detailed hint.
                First attempt → more general hint, second attempt → more specific hint.
                Do NOT give the answer.
                """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content


def generate_explanation_llm(question, correct_answer, options):
    prompt = f"""
                Explain the correct answer.

                Question: {question}
                Correct answer: {correct_answer}
                Options: {options}

                Explain simply why correct is correct and others are wrong.
                """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content



def generate_lesson_llm(module_name, base_content, difficulty):

    prompt = f"""
                You are a tutor.

                Expand this lesson into a clear teaching explanation.

                Module: {module_name}
                Base content: {base_content}
                Student level: {difficulty} (1 beginner → 5 advanced)

                Requirements:
                - Explain clearly
                - Add simple examples
                - Keep it concise (5-8 sentences)
                """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content



def generate_question_llm(topic, difficulty):

    prompt = f"""
                You are a tutor.

                Generate 1 multiple choice question.

                Topic: {topic}
                Difficulty: {difficulty} (1 easy → 5 hard)

                Return format:
                Question:
                A.
                B.
                C.
                Correct Answer:
                """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content

def parse_question(llm_output):

    lines = [l.strip() for l in llm_output.split("\n") if l.strip()]

    content = ""
    options = []
    correct = None

    for l in lines:

        # ✅ lấy question robust
        if "question" in l.lower():
            content = l.split(":", 1)[-1].strip()

        # ✅ parse options
        elif l.startswith(("A.", "B.", "C.")):
            label = l[0].upper()
            text = l[2:].strip()
            options.append((label, text))

        # ✅ parse correct answer robust
        elif "correct" in l.lower():
            correct = l.split(":")[-1].strip().upper().replace(".", "")

    return content, options, correct