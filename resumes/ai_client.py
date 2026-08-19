from decouple import config
from groq import Groq


def get_ai_feedback(resume_text, jd_text, missing_keywords):
    """Return AI-generated resume improvement suggestions as plain text."""
    try:
        client = Groq(api_key=config("GROQ_API_KEY"))

        missing_str = ", ".join(missing_keywords) if missing_keywords else "none"

        response = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a professional resume coach. "
                        "Respond in plain text only, no markdown formatting."
                    ),
                },
                {
                    "role": "user",
                    "content": (
                        f"Job description:\n{jd_text}\n\n"
                        f"Resume text:\n{resume_text}\n\n"
                        f"Missing keywords: {missing_str}\n\n"
                        "Give 3-4 specific, actionable suggestions to improve "
                        "this resume for the job description above."
                    ),
                },
            ],
            temperature=0.7,
            max_tokens=1024,
        )

        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"GROQ API ERROR: {e}")
        return "AI feedback unavailable at this time."
