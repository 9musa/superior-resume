from weasyprint import HTML

def _build_sections(data: dict) -> dict:
    """ predefined HTML sections """
    experience_html = ""
    for job in data.get("experience", []):
        bullets_html = "".join(f"<li>{b}</li>" for b in job.get("bullets", []))
        experience_html += f"""
        <div class="entry">
            <h3>{job.get('title', '')} — {job.get('company', '')}</h3>
            <p class="dates">{job.get('dates', '')}</p>
            <ul>{bullets_html}</ul>
        </div>"""

    education_html = ""
    for edu in data.get("education", []):
        education_html += f"""
        <div class="entry">
            <h3>{edu.get('degree', '')}</h3>
            <p>{edu.get('school', '')} — {edu.get('dates', '')}</p>
        </div>"""

    projects_html = ""
    for p in data.get("projects", []):
        projects_html += f"""
        <div class="entry">
            <h3>{p.get('name', '')}</h3>
            <p>{p.get('description', '')}</p>
        </div>"""

    skills_html = ", ".join(data.get("skills", []))

    languages_html = ", ".join(data.get("languages", []))

    return {
        "experience": experience_html,
        "education": education_html,
        "projects": projects_html,
        "skills": skills_html,
        "languages": languages_html,
    }

# Classic
def render_classic(data: dict) -> str:
    s = _build_sections(data)
    return f"""
    <html><head><style>
        body {{ font-family: Georgia, serif; font-size: 10.5pt; margin: 40px; color: #222; }}
        h1 {{ font-size: 20pt; text-align: center; margin-bottom: 2px; }}
        h2 {{ font-size: 12pt; border-bottom: 1px solid #333; margin-top: 18px; }}
        .contact {{ text-align: center; color: #555; font-size: 9.5pt; }}
        ul {{ margin: 4px 0 10px 18px; }}
    </style></head><body>
        <h1>{data.get('full_name','')}</h1>
        <p class="contact">{data.get('contact_info','')}</p>
        {'<h2>Summary</h2><p>'+data['summary']+'</p>' if data.get('summary') else ''}
        {'<h2>Experience</h2>'+s['experience'] if s['experience'] else ''}
        {'<h2>Education</h2>'+s['education'] if s['education'] else ''}
        {'<h2>Projects</h2>'+s['projects'] if s['projects'] else ''}
        {'<h2>Skills</h2><p>'+s['skills']+'</p>' if s['skills'] else ''}
        {'<h2>Languages</h2><p>'+s['languages']+'</p>' if s['languages'] else ''}
    </body></html>"""

# Modern
def render_modern(data: dict) -> str:
    s = _build_sections(data)
    return f"""
    <html><head><style>
        body {{ font-family: 'Helvetica', sans-serif; font-size: 10.5pt; margin: 40px; color: #1a1a1a; }}
        h1 {{ font-size: 22pt; color: #2563eb; margin-bottom: 2px; }}
        h2 {{ font-size: 12pt; color: #2563eb; text-transform: uppercase; letter-spacing: 1px; margin-top: 18px; }}
        .contact {{ color: #666; font-size: 9.5pt; }}
        ul {{ margin: 4px 0 10px 18px; }}
    </style></head><body>
        <h1>{data.get('full_name','')}</h1>
        <p class="contact">{data.get('contact_info','')}</p>
        {'<h2>Summary</h2><p>'+data['summary']+'</p>' if data.get('summary') else ''}
        {'<h2>Experience</h2>'+s['experience'] if s['experience'] else ''}
        {'<h2>Education</h2>'+s['education'] if s['education'] else ''}
        {'<h2>Projects</h2>'+s['projects'] if s['projects'] else ''}
        {'<h2>Skills</h2><p>'+s['skills']+'</p>' if s['skills'] else ''}
        {'<h2>Languages</h2><p>'+s['languages']+'</p>' if s['languages'] else ''}
    </body></html>"""

# Minimal
def render_minimal(data: dict) -> str:
    s = _build_sections(data)
    return f"""
    <html><head><style>
        body {{ font-family: 'Courier New', monospace; font-size: 10pt; margin: 50px; color: #000; }}
        h1 {{ font-size: 16pt; margin-bottom: 0; }}
        h2 {{ font-size: 10pt; text-transform: uppercase; margin-top: 20px; border-top: 1px solid #000; padding-top: 4px; }}
        ul {{ margin: 4px 0 10px 18px; }}
    </style></head><body>
        <h1>{data.get('full_name','')}</h1>
        <p>{data.get('contact_info','')}</p>
        {'<h2>Summary</h2><p>'+data['summary']+'</p>' if data.get('summary') else ''}
        {'<h2>Experience</h2>'+s['experience'] if s['experience'] else ''}
        {'<h2>Education</h2>'+s['education'] if s['education'] else ''}
        {'<h2>Projects</h2>'+s['projects'] if s['projects'] else ''}
        {'<h2>Skills</h2><p>'+s['skills']+'</p>' if s['skills'] else ''}
        {'<h2>Languages</h2><p>'+s['languages']+'</p>' if s['languages'] else ''}
    </body></html>"""

# Technical
def render_technical(data: dict) -> str:
    s = _build_sections(data)
    projects_html = "".join(
        f"<div class='entry'><h3>{p.get('name','')}</h3><p>{p.get('description','')}</p></div>"
        for p in data.get("projects", [])
    )
    return f"""
    <html><head><style>
        body {{ font-family: 'Helvetica', sans-serif; font-size: 10pt; margin: 35px; color: #222; }}
        h1 {{ font-size: 18pt; margin-bottom: 2px; }}
        h2 {{ font-size: 11pt; background: #f0f0f0; padding: 3px 6px; margin-top: 16px; }}
        ul {{ margin: 4px 0 10px 18px; }}
    </style></head><body>
        <h1>{data.get('full_name','')}</h1>
        <p>{data.get('contact_info','')}</p>
        {'<h2>Skills</h2><p>'+s['skills']+'</p>' if s['skills'] else ''}
        {'<h2>Projects</h2>'+s['projects'] if s['projects'] else ''}
        {'<h2>Experience</h2>'+s['experience'] if s['experience'] else ''}
        {'<h2>Education</h2>'+s['education'] if s['education'] else ''}
        {'<h2>Languages</h2><p>'+s['languages']+'</p>' if s['languages'] else ''}
    </body></html>"""

# Creative
def render_creative(data: dict) -> str:
    s = _build_sections(data)
    return f"""
    <html><head><style>
        body {{ font-family: 'Helvetica', sans-serif; font-size: 10.5pt; margin: 0; color: #222; }}
        .header {{ background: #1e293b; color: white; padding: 30px 40px; }}
        .header h1 {{ font-size: 22pt; margin: 0; }}
        .body {{ padding: 20px 40px; }}
        h2 {{ font-size: 12pt; color: #1e293b; border-bottom: 2px solid #1e293b; margin-top: 16px; }}
        ul {{ margin: 4px 0 10px 18px; }}
    </style></head><body>
        <div class="header">
            <h1>{data.get('full_name','')}</h1>
            <p>{data.get('contact_info','')}</p>
        </div>
        <div class="body">
            {'<h2>Summary</h2><p>'+data['summary']+'</p>' if data.get('summary') else ''}
            {'<h2>Experience</h2>'+s['experience'] if s['experience'] else ''}
            {'<h2>Education</h2>'+s['education'] if s['education'] else ''}
            {'<h2>Skills</h2><p>'+s['skills']+'</p>' if s['skills'] else ''}
            {'<h2>Languages</h2><p>'+s['languages']+'</p>' if s['languages'] else ''}
        </div>
    </body></html>"""


TEMPLATES = {
    "classic": render_classic,
    "modern": render_modern,
    "minimal": render_minimal,
    "technical": render_technical,
    "creative": render_creative,
}


def render_resume_pdf(data: dict, template: str = "classic") -> bytes:
    render_fn = TEMPLATES.get(template, render_classic) # appropriate render function
    html_content = render_fn(data)
    return HTML(string=html_content).write_pdf() # renders pdf from file obj