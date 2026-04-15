# Project Context

This project is a local QA agent.

Goal:
- Read a project's context
- Generate a QA plan using a local LLM
- Run API, browser, and load checks
- Produce a simple report

Current environment:
- API base URL: http://localhost:8000
- UI base URL: http://localhost:3000

Constraints:
- No destructive actions
- Local development only
- Focus on QA first