# AGENTS.md - Plan Mode Architecture Rules

This file provides planning-specific guidance for agents working in this repository.

## System Architecture (Non-Obvious Constraints)

**Critical**: AI agent is reasoning engine only - does NOT execute code directly. Writes tests/fixes → subprocess sandbox executes → returns stdout/stderr.

## Component Interaction Pattern

- Component A (Django): State management, API endpoints (not yet implemented)
- Component B (mcp_server.py): MCP bridge with 3 tools (write_file, run_test, report_to_boss)
- Component C (Subprocess): Execution sandbox for pytest
- report_to_boss hardcoded to http://localhost:8000/api/report/ (requires Django running)

## Database Architecture

Uses SQLite3 (db.sqlite3) as configured in BuildCheck_AI/settings.py.

## Current Implementation State

- testing app: skeleton only (empty models/views)
- BugTicket model: not implemented yet
- API endpoints: not created yet
- BUG_TO_TEST_PLAN.md contains actual roadmap (6 steps)

## Testing Architecture

pytest via subprocess (not Django's unittest) - no test discovery, explicit file paths required.

## Dependency Management

No requirements.txt or pyproject.toml - dependencies installed manually: pytest, mcp, requests, django