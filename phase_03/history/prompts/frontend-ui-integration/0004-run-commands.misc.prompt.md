---
ID: "0004"
TITLE: "Run Commands"
STAGE: "misc"
DATE_ISO: "2026-02-03"
SURFACE: "agent"
MODEL: "gemini-2.0-pro-exp-02-05"
FEATURE: "frontend-ui-integration"
BRANCH: "main"
USER: "user"
COMMAND: "run_command"
LABELS: ["run", "commands", "setup"]
LINKS: "null"
FILES_YAML: 
 - "backend/CLAUDE.md"
 - "frontend/package.json"
TESTS_YAML: "null"
PROMPT_TEXT: "tell me the command of both frontend and backend run"
RESPONSE_TEXT: "Backend: `uvicorn main:app --reload --port 8000`\nFrontend: `npm run dev`"
OUTCOME: "Provided run commands for both services."
---

# Run Commands

User requested commands to run both frontend and backend.

## Prompt

> tell me the command of both frontend and backend run

## Response

Here are the commands to run the application:

### Backend (FastAPI)
Run from `backend/` directory:
```bash
uvicorn main:app --reload --port 8000
```

### Frontend (Next.js)
Run from `frontend/` directory:
```bash
npm run dev
```
