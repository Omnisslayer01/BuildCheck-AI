# AGENTS.md - Advanced Mode Rules

This file provides advanced coding-specific guidance for agents working in this repository.

## Critical Execution Model

You do NOT run code directly. You write tests/fixes and hand them to subprocess sandbox (mcp_server.py) which returns stdout/stderr.

## MCP Tools for Code Execution

- `write_file(file_name, content)` - Write code to filesystem
- `run_test(file_name)` - Execute pytest via subprocess (not Django's unittest)
- `report_to_boss(message)` - POST to http://localhost:8000/api/report/

## Database Operations

Use SQLite3 syntax. Database file: db.sqlite3

## Testing Requirements

- Framework: pytest (install manually: `pip install pytest mcp requests django`)
- Execution: subprocess.run(["pytest", file_name])
- No test discovery - explicit file paths required

## Django App Structure

- testing app has skeleton only (empty models/views)
- URLs: testing.urls included at root level in BuildCheck_AI/urls.py
- No CSRF protection on API endpoints (uses @csrf_exempt for MCP integration)

## Advanced Mode Features

Access to MCP and Browser tools available (unlike Code mode).