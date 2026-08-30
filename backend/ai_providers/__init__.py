from . import gemini, groq

async def superiorise_with_fallback(resume_text: str, job_description: str) -> dict:
    attempts = [
        ("gemini", lambda: gemini.superiorise(resume_text, job_description)),
        ("groq-llama", lambda: groq.superiorise(resume_text, job_description, model="llama-3.3-70b-versatile")),
        ("groq-qwen", lambda: groq.superiorise(resume_text, job_description, model="qwen3-32b")),
    ]

    last_error = None
    for name, attempt in attempts:
        try:
            return await attempt()
        except Exception as e:
            last_error = e
            continue