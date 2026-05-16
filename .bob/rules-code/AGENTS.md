# AGENTS.md - Code Mode Rules

This file provides coding-specific guidance for agents working in this repository.

## Critical Execution Model

You do NOT run code directly. You write tests/fixes and hand them to subprocess sandbox (mcp_server.py) which returns stdout/stderr.

## MCP Tools for Code Execution

- `write_file(file_name, content)` - Write code to filesystem
- `run_test(file_name)` - Execute pytest via subprocess (not Django's unittest)
- `report_to_boss(ticket_id, status)` - POST to http://localhost:8000/api/update-status/

**Critical**: `report_to_boss` requires `ticket_id` (int) and `status` (str), not a generic message string. Valid statuses: 'analyzing', 'test_failed', 'fixed' (hardcoded in testing/views.py).

## Testing Requirements

- Framework: pytest (not Django's unittest)
- Execution: subprocess.run(["pytest", file_name])
- No test discovery - explicit file paths required

## Django App Structure

- testing.urls included at root level in BuildCheck_AI/urls.py (no /testing/ prefix)
- API endpoints use @csrf_exempt for MCP integration

## Code Mode Restrictions

No access to MCP and Browser tools (use Advanced mode for those).