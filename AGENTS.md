# AGENTS.md

This file provides guidance to agents when working with code in this repository.

## Architecture Constraints (Non-Obvious)

**Critical**: You are the AI reasoning engine invoked via MCP Server - you do NOT execute code directly. You write tests/fixes and hand them to subprocess sandbox which returns stdout/stderr.

## MCP Server Tools (mcp_server.py)

Three custom tools with specific signatures:
- `write_file(file_name, content)` - Write content to filesystem
- `run_test(file_name)` - Execute pytest via subprocess (not Django's unittest)
- `report_to_boss(ticket_id, status)` - POST to http://localhost:8000/api/update-status/

**Critical**: `report_to_boss` requires `ticket_id` (int) and `status` (str), not a generic message string. Valid statuses: 'analyzing', 'test_failed', 'fixed' (hardcoded in testing/views.py).

**Important**: Django dev server must be running on port 8000 for report_to_boss to work.

## Testing Framework

Uses **pytest** (not Django's default unittest). Tests executed via subprocess.run(["pytest", file_name]).

**Critical**: No test discovery - explicit file paths required. You must specify the exact test file path.

## Environment Configuration

Uses django-environ for environment variables. Requires .env file with SECRET_KEY and DEBUG settings (not exposed in settings.py).

## URL Routing

testing app URLs included at root level via `path('', include('testing.urls'))` in BuildCheck_AI/urls.py (no /testing/ prefix).

API endpoints use @csrf_exempt for MCP integration.