def build_resume_prompt(resume_text: str, job_desc: str) -> str:
    return f"""You are a professional resume writer. Analyze the following text.

First, decide if this is actually resume/CV content (work history, education, 
skills — a person describing their professional background). If it is NOT a 
resume (e.g. a grocery list, random notes, unrelated text), set 
is_valid_resume to false and explain why in rejection_reason.

If it IS a resume, improve it to align with this target role/job description:
"{job_desc}"

Tailor relevant experience and skills toward what this description emphasizes, 
strengthen wording, use strong action verbs, keep all facts truthful (never invent experience). 
If the person has no work experience, return an empty experience list — do 
not fabricate jobs. Fill in every field you can find; leave fields empty 
(not fabricated) if the info isn't present.

When extracting skills, keep these categories strictly separate:
- "skills": technical/professional skills and tools (e.g. Python, Figma, project management)
- "languages": spoken/written human languages only (e.g. English, Spanish, Mandarin)
Never mix programming languages or tools into the "languages" field, and never 
put spoken languages into "skills".

TEXT:
{resume_text}
"""