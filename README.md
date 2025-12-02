
# AI-CRM-HCP-Module-completed
=======
# AI-CRM-HCP — Complete Task 1 Project (Runnable)

This project implements the AI-First CRM HCP Module (LogInteractionScreen) and is prepared to run locally with zero external API keys required.

**What's included**
- Frontend: React + Redux (Vite)
- Backend: FastAPI (uses SQLite by default)
- Simple "LangGraph-like" agent wrapper that uses Groq if GROQ_API_KEY is provided, otherwise uses a local mock summarizer so the app runs without errors.
- Dockerfiles and docker-compose (optional). The docker-compose uses the backend standalone (SQLite), so no Postgres required for local testing.
- README with run instructions.

**Notes**
- If you want to use Groq (gemma2-9b-it), set `GROQ_API_KEY` in `.env` and the backend will attempt to call Groq. If not set, a local summarizer will be used automatically.
- The project uses SQLite for simplicity to ensure it runs out-of-the-box. For production, swap DATABASE_URL to Postgres/MySQL and update the SQLAlchemy URL.

# AI-First CRM – HCP Module

## Project Description
This project is an AI-powered CRM module for managing HCP (Health Care Professional) interactions.
It allows sales representatives to log interactions and receive AI-based suggestions.

## Tech Stack
- Frontend: React (Vite)
- Backend: FastAPI
- AI Endpoint: REST API (Chat service)
- Database: (mention if added)

## Features
- Log HCP interactions
- AI Assistant for interaction analysis
- REST API integration
- Responsive UI
- Swagger API documentation

## How to Run Backend
```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload

Backend runs on: http://127.0.0.1:8000
API Docs: http://127.0.0.1:8000/docs

## How to Run Frontend
cd frontend
npm install
npm run dev

Frontend runs on: http://localhost:5173

# AI CRM HCP Module

An AI-first Customer Relationship Management module for managing HCP (Healthcare Professional) interactions with intelligent chat assistance.

## Features
- Log interactions with HCP
- AI Assistant for interaction analysis
- FastAPI backend
- React + Vite frontend
- Docker ready setup

## Project Structure

