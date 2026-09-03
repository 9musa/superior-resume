# Superior Resume

![Python](https://img.shields.io/badge/Python-3.14-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white)
![React](https://img.shields.io/badge/React-61DAFB?logo=react&logoColor=black)
![License](https://img.shields.io/badge/license-MIT-blue)

AI powered resume enhancer.

## Overview
Superior Resume analyses your resume through LLMs and renders a new one better suited to your target role.

## Preview
*Coming soon - UI still in progress*

## To Do
- [ ] Finish wiring custom exceptions across all endpoints (base cases covered, several still using generic error handling)
- [ ] Add frontend template selector (backend supports 5 templates, no UI to choose one yet)
- [ ] Password reset, account page, job history
- [ ] Add rate limiting
- [ ] Prompt-injection hardening
- [ ] General UI polish

## Features
- AI-driven resume analysis and rewriting via Gemini, with automatic fallback to Groq-hosted models if unavailable
- Structured output
- Multiple downloadable resume templates
- Optional user accounts (JWT-based auth) with guest usage supported
- Asynchronous job processing with live status polling

## Built With
- [Python](https://www.python.org/) - Core programming language.
- [FastAPI](https://fastapi.tiangolo.com/) - Backend web framework.
- [React](https://react.dev/) - Frontend UI library.
- [Vite](https://vite.dev/) - Frontend build tool.
- [NeonDB](https://neon.tech/) - Serverless Postgres database.
- [Gemini API](https://ai.google.dev/) - Primary AI provider for resume enhancement.
- [Groq](https://groq.com/) - Fallback AI provider (Llama, Qwen).
- [WeasyPrint](https://weasyprint.org/) - HTML-to-PDF rendering.

## Getting Started

### Prerequisites

#### For Developers
Ensure you have Python and Node.js installed on your machine:
```bash
python --version
node --version
```

### Installation

#### For Developers
Clone this repository to your local machine:
```bash
   git clone https://github.com/9musa/superior-resume.git
   cd superior-resume
```

Set up the backend:
```bash
   cd backend
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
```

Set up the frontend:
```bash
   cd ../frontend
   npm install
```

Add your environment variables (`backend/.env` and `frontend/.env`) — see `.env.example` for required keys (database URL, JWT secret, Gemini/Groq API keys).

Run both servers:
```bash
   # terminal 1
   cd backend && uvicorn main:app --reload

   # terminal 2
   cd frontend && npm run dev
```

## Authors
Developed by [9musa](https://github.com/9musa) under Verelous Labs.

## License
Superior Resume is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.