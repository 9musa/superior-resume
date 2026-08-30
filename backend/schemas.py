RESUME_SCHEMA = {
    "type": "object",
    "properties": {
        "is_valid_resume": {"type": "boolean"},
        "rejection_reason": {"type": "string"},
        "full_name": {"type": "string"},
        "contact_info": {"type": "string"},
        "summary": {"type": "string"},
        "experience": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "title": {"type": "string"},
                    "company": {"type": "string"},
                    "dates": {"type": "string"},
                    "bullets": {"type": "array", "items": {"type": "string"}},
                },
            },
        },
        "education": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "school": {"type": "string"},
                    "degree": {"type": "string"},
                    "dates": {"type": "string"},
                },
            },
        },
        "skills": {"type": "array", "items": {"type": "string"}},
        "languages": {"type": "array", "items": {"type": "string"}},
        "projects": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "description": {"type": "string"},
                },
            },
        },
    },
    "required": ["is_valid_resume", "full_name", "summary", "experience", "education", "skills"],
}

#OpenAI style LLMs
RESUME_SCHEMA_STRICT = {
    "type": "object",
    "properties": {
        "is_valid_resume": {"type": "boolean"},
        "rejection_reason": {"type": ["string", "null"]},
        "full_name": {"type": ["string", "null"]},
        "contact_info": {"type": ["string", "null"]},
        "summary": {"type": ["string", "null"]},
        "experience": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "title": {"type": ["string", "null"]},
                    "company": {"type": ["string", "null"]},
                    "dates": {"type": ["string", "null"]},
                    "bullets": {"type": "array", "items": {"type": "string"}},
                },
                "required": ["title", "company", "dates", "bullets"],
                "additionalProperties": False,
            },
        },
        "education": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "school": {"type": ["string", "null"]},
                    "degree": {"type": ["string", "null"]},
                    "dates": {"type": ["string", "null"]},
                },
                "required": ["school", "degree", "dates"],
                "additionalProperties": False,
            },
        },
        "skills": {"type": "array", "items": {"type": "string"}},
        "languages": {"type": "array", "items": {"type": "string"}},
        "projects": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "name": {"type": ["string", "null"]},
                    "description": {"type": ["string", "null"]},
                },
                "required": ["name", "description"],
                "additionalProperties": False,
            },
        },
    },
    "required": [
        "is_valid_resume", "rejection_reason", "full_name", "contact_info",
        "summary", "experience", "education", "skills", "languages", "projects",
    ],
    "additionalProperties": False,
}