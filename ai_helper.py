import groq
import os

client = groq.Groq(api_key=os.environ.get("GROQ_API_KEY"))

def generate_note(topic):
    
    """
Generate study notes using Groq AI.
"""

    prompt = f"""
Generate short study notes on the topic: {topic}

Rules:
1. Use simple language.
2. Maximum 120 words.
3. Student friendly explanation.
4. Return only the note.
"""
    try:
        response = client.chat.completions.create(

        model="openai/gpt-oss-120b",

        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]

    )

        return response.choices[0].message.content
    
    except Exception as e:
        return f"Unable to connect to AI service.\nError: {e}"




def summarize_note(note):
    """
Generate a short summary of a note.
    """

    prompt = f"""
Summarize the following study note.

Rules:
1. Maximum 60 words.
2. Keep important points.
3. Use simple language.
4. Return only the summary.

Study Note:

{note}
"""
    
    try:
        response = client.chat.completions.create(

        model="openai/gpt-oss-120b",

        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]

    )

        return response.choices[0].message.content
    
    except Exception as e:
        return f"Unable to connect to AI service.\nError: {e}"


def generate_quiz(note):
    
    """
Generate multiple-choice questions from a note.
    """

    prompt = f"""
Generate 5 multiple choice questions from the following study note.

Rules:

1. Each question should have 4 options.
2. Mention the correct answer.
3. Keep questions simple.
4. Return only the quiz.

Study Note:

{note}
"""
    try:
        response = client.chat.completions.create(

        model="openai/gpt-oss-120b",

        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]

    )

        return response.choices[0].message.content
    
    except Exception as e:
        return f"Unable to connect to AI service.\nError: {e}"

