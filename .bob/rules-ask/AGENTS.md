# AGENTS.md - Ask Mode Documentation Rules

This file provides documentation-specific guidance for agents working in this repository.

## Documentation Mismatches (Non-Obvious)

- **README describes full system** but only skeleton exists (empty models/views in testing app)
- **BUG_TO_TEST_PLAN.md is the actual roadmap** - shows what's planned vs implemented

## Architecture Context

- AI agent is invoked via MCP Server, does NOT execute code directly
- Subprocess sandbox pattern: AI writes → sandbox executes → returns output
- Three MCP tools: write_file, run_test, report_to_boss

## Project State (Important for Questions)

- testing app: skeleton only (no models, views, or API endpoints yet)
- BugTicket model: not implemented (planned in BUG_TO_TEST_PLAN.md)
- Dependencies: no requirements.txt (manual install: pytest, mcp, requests, django)
- Django dev server must run on port 8000 for MCP report_to_boss tool

## Testing Framework

Uses pytest (not Django's default unittest) - executed via subprocess, not test discovery.

## URL Structure

Counterintuitive: testing app URLs included at root level (`path('', include('testing.urls'))`) in BuildCheck_AI/urls.py