import os
import json
from google.genai import types
from dotenv import load_dotenv
from google import genai
from schemas import RESUME_SCHEMA
from .prompt import build_resume_prompt

load_dotenv()
GEMINI_API_KEY = os.environ["GEMINI_API_KEY"]
client = genai.Client(api_key=GEMINI_API_KEY)

async def superiorise(resume_text: str, job_desc: str):
    prompt = build_resume_prompt(resume_text, job_desc)

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=RESUME_SCHEMA,
        ),
    )

    return json.loads(response.text)