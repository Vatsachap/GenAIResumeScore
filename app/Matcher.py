import json
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_resume_score(resume_text, job_text):
    prompt = f"""
Evaluate this resume against the job description.

Job Description:
{job_text}

Resume:
{resume_text}

Respond ONLY in this exact JSON format (no extra text, no markdown):
{{"score": <score out of 100>, "reasoning": "<summary>"}}
"""

    messages = [
        {"role": "system", "content": "You are a helpful assistant that MUST respond ONLY in strict JSON format as specified."},
        {"role": "user", "content": prompt}
    ]

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            temperature=0
        )

        content = response.choices[0].message.content
        print("Raw response content:", content)  # Debug output

        # Parse JSON strictly
        result = json.loads(content)
        return result

    except json.JSONDecodeError as e:
        return {
            "score": 0,
            "reasoning": f"Failed to parse JSON response: {str(e)}. Raw content: {content}"
        }
    except Exception as e:
        return {
            "score": 0,
            "reasoning": f"Failed to score: {str(e)}"
        }


