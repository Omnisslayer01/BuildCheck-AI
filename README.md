# 🚀 BuildCheck AI

**An AI-powered project evaluator, automated debugging system, and active server security agent.**

BuildCheck AI accelerates software development from ideation to production. It acts as an intelligent safety net that audits business viability, evaluates technical readiness, autonomously resolves bugs using a Test-Driven Development (TDD) workflow, and actively secures the deployment environment.

**Core AI Engine:** Built with [IBM Bob](https://ibm.com) and integrated natively via the **Model Context Protocol (MCP)**.

---

## 🧠 For AI Coding Agents Reading This Repository
If you are an AI assistant (like IBM Bob) assisting with this codebase, please note the following architectural constraints:
1. **Role:** You are the core reasoning engine. You will be invoked via the Python MCP Server (`Component B`) to evaluate code, generate tests, and provide patches.
2. **Execution:** You do *not* run code directly. You write code (tests/fixes) and hand it to the `subprocess` Sandbox (`Component C`), which returns `stdout`/`stderr` back to you.
3. **State Management:** All state (Bug status, Security events) is managed by Django (`Component A`) and persisted in SQLlite.
4. **Current Focus:** The primary operational loop is the **Bug-to-Test Execution Loop** defined in Section 4.

---

## 🛠️ Technology Stack (PMND + AI)

* **Python:** Core language for the backend, testing sandboxes, and MCP Server.
* **sqllite:** Relational database storing evaluation histories, bug logs, and security events.
* **Nginx:** Web server and reverse proxy handling HTTP/HTTPS routing.
* **Django:** Backend framework handling business logic, API endpoints, and state management.
* **HTMX & TailwindCSS:** Frontend UI layer for dynamic, server-side rendered, asynchronous DOM updates.
* **IBM Bob + MCP:** The AI reasoning engine, connected natively to the backend via a custom Python Model Context Protocol Server.
* **Pytest + Subprocess:** The isolated execution sandbox for AI-generated code validation.

---

## 📦 Core Modules

### 1. The Dual-Lens Evaluator (VC + CTO Mode)
Developers often build features without validating if the business logic is sound or if the code is production-ready. BuildCheck AI solves this by acting as an autonomous Product Strategist and Enterprise CTO.

**How to test this feature:**
We have included a `demo_startup/` folder with sample code (or you can use your own code! Just paste your entire project folder into the 'demo_startup' folder after removing the existing files).

1. Ensure the Django server is running (`python manage.py runserver`) and the Dashboard is open.
2. Open IBM Bob in your IDE.
3. Type `@evaluate.md Execute this` to load our Master Prompt, and press Enter to execute.

**What happens:**
IBM Bob will analyze the startup's product-market fit and technical debt simultaneously. It will invoke our custom MCP Server tool (`submit_business_lens`) to send a secure Webhook to the Django backend. You will see the purple "Business Lens" card on the web dashboard instantly update with an AI-generated Viability Score and Executive Summary.

### 2. 🚢 Ship Check (Technical Readiness)
Acts as an AI Senior Software Engineer.
* **Inputs:** Codebase structure and existing files.
* **Outputs:** Technical readiness score, code quality observations, missing edge cases/tests, security risks, and prioritized engineering fixes.

### 3. 🐛 Bug-to-Test Workflow (Automated TDD Resolution)
An autonomous loop that turns user complaints into verified code fixes.
* **Inputs:** User-provided bug report or error log.
* **Outputs:** AI-generated failing test, AI-generated code fix, execution logs, and resolution diff.

### 4. 🛡️ Active Security & Threat Mitigation Agent
A parallel, autonomous background daemon running on the server.
* **Inputs:** Real-time server logs, network traffic, SSH logs, system resource utilization (CPU/GPU).
* **Action:** Actively monitors and blocks brute-force attempts, malware signatures, honeypot triggers, cryptomining, and anomalous SSH access via firewall rules (e.g., `iptables`). Alerts are logged to the Django backend.

---

## 🏗️ System Architecture

* **Component A (Core Django Backend):** The brain and persistence layer. Orchestrates HTTP requests, handles database transactions (Models: `ProjectContext`, `EvaluationReport`, `BugTicket`, `SecurityEvent`), and serves HTMX fragments.
* **Component B (Python MCP Server):** The AI Bridge. Exposes registered tools (e.g., `audit_project`, `read_bug_and_locate`) to IBM Bob, allowing the AI to interact with Django data and the local file system.
* **Component C (Execution Sandbox):** The local testing environment. Prompts Bob for a test -> executes via `subprocess` -> captures logs -> prompts Bob for a fix -> re-runs the test.
* **Component D (Frontend/Proxy):** Nginx routes traffic. HTMX dynamically updates UI components (e.g., swapping a pending spinner for a "Bug Fixed" badge) based on database state.
* **Component E (Security Daemon):** Standalone monitoring service that parses logs, applies firewall rules, and posts threat data to the Django API.

---

## 🔄 The Bug-to-Test Execution Loop (Data Flow)

The heart of BuildCheck AI is its autonomous debugging loop. Here is exactly how a bug is processed:

1. **Ingestion:** User submits a bug report via the Django UI (e.g., *"App crashes on empty cart"*).
2. **State Initialization:** Django creates a `BugTicket` in SQLlite with `status = analyzing`.
3. **AI Contextualization:** Django triggers the Python MCP client, handing the bug text and project context to IBM Bob.
4. **Test Generation:** IBM Bob generates a `pytest` script to reproduce the bug. Django writes this script to the execution sandbox.
5. **Execution (Validation of Failure):** Component C runs the test via `subprocess`. It captures the expected failure stack trace.
6. **State Update 1:** SQLlite `BugTicket` status updates to `test_failed`. HTMX dynamically updates the UI to show a Red "Test Failing" alert.
7. **Fix Generation:** Python MCP client sends the captured stack trace back to IBM Bob. Bob generates the code patch.
8. **Execution (Validation of Fix):** Component C applies the patch and re-runs the test via `subprocess`. The test passes.
9. **State Update 2:** SQLlite `BugTicket` status updates to `fixed`.
10. **Resolution Delivery:** HTMX dynamically updates the UI to a Green "Bug Fixed" alert and displays the code diff to the user for final approval.

---

## 🚀 Setup & Installation (Local Development)

*(Coming soon: Instructions on how to set up the Python virtual environment, apply Django migrations, start the MCP server, and configure IBM Bob).*