# AGENTS.md - Plan Mode Rules

This file provides planning-specific guidance for agents working in this repository.

## Architecture Constraints (Non-Obvious)

**Critical**: System uses subprocess sandbox pattern - AI agent writes tests/fixes but doesn't execute them directly. MCP server (mcp_server.py) bridges AI reasoning with code execution via subprocess.

## MCP Server Architecture

Three-tool design pattern:
- `write_file(file_name, content)` - Filesystem operations
- `run_test(file_name)` - Pytest execution (not Django unittest)
- `report_to_boss(ticket_id, status)` - Status updates to Django API

**Important**: `report_to_boss` requires structured parameters `(ticket_id: int, status: str)` with hardcoded valid statuses: 'analyzing', 'test_failed', 'fixed' (defined in testing/views.py).

## Testing Architecture

Pytest chosen over Django's unittest for subprocess compatibility. No test discovery mechanism - explicit file paths required.

## URL Routing Pattern

testing app URLs mounted at root level (no /testing/ prefix) - counterintuitive but intentional for API simplicity.

## Environment Management

django-environ pattern for SECRET_KEY and DEBUG configuration via .env file (not exposed in settings.py).

## API Integration

Django dev server must run on port 8000 for MCP server's report_to_boss to function. API endpoints use @csrf_exempt for external MCP integration.