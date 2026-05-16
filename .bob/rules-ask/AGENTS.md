# AGENTS.md - Ask Mode Rules

This file provides documentation-specific guidance for agents working in this repository.

## Project Architecture (Non-Obvious)

**Critical**: AI agent is invoked via MCP Server - does NOT execute code directly. Tests/fixes are handed to subprocess sandbox which returns stdout/stderr.

## MCP Server Integration

MCP server (mcp_server.py) provides three tools that bridge AI reasoning with code execution:
- `write_file(file_name, content)` - Filesystem writes
- `run_test(file_name)` - Pytest execution via subprocess
- `report_to_boss(ticket_id, status)` - Django API updates

**Important**: `report_to_boss` signature is `(ticket_id: int, status: str)`, not a generic message parameter.

## Testing Framework (Non-Standard)

Uses pytest instead of Django's default unittest. No test discovery - explicit file paths required for subprocess.run(["pytest", file_name]).

## URL Structure (Counterintuitive)

testing app URLs mounted at root level (not /testing/ prefix) via `path('', include('testing.urls'))` in BuildCheck_AI/urls.py.

## Environment Configuration

Uses django-environ for SECRET_KEY and DEBUG from .env file (not hardcoded in settings.py).