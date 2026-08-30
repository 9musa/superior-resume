import os, json
from groq import Groq
from dotenv import load_dotenv
from schemas import RESUME_SCHEMA_STRICT
from .prompt import build_resume_prompt


load_dotenv()
GROQ_API_KEY = os.environ["GROQ_API_KEY"]
client = Groq(api_key=GROQ_API_KEY)

async def superiorise(resume_text: str, job_desc: str, model: str = "llama-3.3-70b-versatile") -> dict:
    prompt = build_resume_prompt(resume_text, job_desc)
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        response_format={
            "type": "json_schema",
            "json_schema": {"name": "resume_schema", "strict": True, "schema": RESUME_SCHEMA_STRICT},
        },
    )
    return json.loads(response.choices[0].message.content)