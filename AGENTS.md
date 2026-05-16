# AGENTS.md

This file provides guidance to agents when working with code in this repository.

## Architecture Constraints (Non-Obvious)

**Critical**: You are the AI reasoning engine invoked via MCP Server - you do NOT execute code directly. You write tests/fixes and hand them to the subprocess sandbox which returns stdout/stderr.

## Database Configuration

Uses SQLite3 (db.sqlite3) as configured in BuildCheck_AI/settings.py.

## MCP Server Tools (mcp_server.py)

Three custom tools available:
- `write_file(file_name, content)` - Write content to filesystem
- `run_test(file_name)` - Execute pytest on a file via subprocess
- `report_to_boss(message)` - POST to http://localhost:8000/api/report/ (hardcoded endpoint)

**Important**: Django dev server must be running on port 8000 for report_to_boss to work.

## Testing Framework

Uses **pytest** (not Django's default unittest). Tests executed via subprocess.run(["pytest", file_name]).

## Dependencies

No requirements.txt or pyproject.toml exists. Manual installation required:
```bash
pip install pytest mcp requests django
```

## Project State

- testing app has empty models/views (skeleton only)
- BugTicket model not yet implemented (see BUG_TO_TEST_PLAN.md for roadmap)
- API endpoints not yet created
- Secret key exposed in settings.py (development only - change for production)

## URL Routing

testing app URLs included at root level via `path('', include('testing.urls'))` in BuildCheck_AI/urls.py