# Project Context & Architecture Document: BuildCheck AI

**Project Name:** BuildCheck AI
**Objective:** An AI-powered project evaluator, automated debugging system, and active server security agent. It accelerates software development from ideation to production by auditing business viability, technical readiness, autonomously resolving bugs via Test-Driven Development (TDD), and actively securing the deployment environment.
**Core AI Engine:** IBM Bob (integrated via Model Context Protocol - MCP)

---

## 1. Technology Stack (PMND + AI)
*   **Backend Framework:** Python / Django (Handles business logic, API endpoints, testing sandboxes, and state management).
*   **Database:** MySQL (Relational storage for evaluation histories, generated test cases, bug logs, and security incident logs).
*   **Web Server / Proxy:** Nginx (Handles HTTP/HTTPS routing, serves static assets, and proxies dynamic requests to the WSGI server).
*   **Frontend UI:** Django Templates + HTMX + TailwindCSS (Server-side rendered UI with dynamic, asynchronous DOM updates).
*   **AI Integration Layer:** Python Model Context Protocol (MCP) Server (Natively connects the Django backend to the IBM Bob IDE).
*   **Execution Sandbox:** Python `subprocess` module + `pytest` / `unittest` (Isolated execution of AI-generated code).

---

## 2. Core Modules

### Module 1: Venture Check (Business Viability)
*   **Inputs:** App name, problem statement, target users, proposed solution, monetization strategy, competitors.
*   **Outputs:** Clarity scores (problem, user), market urgency score, differentiation score, execution risk score, and MVP improvement suggestions.

### Module 2: Ship Check (Technical Readiness)
*   **Inputs:** Codebase structure, existing files.
*   **Outputs:** Technical readiness score, code quality observations, missing edge cases/tests, security risks, deployment checklist, and prioritized engineering fixes.

### Module 3: Bug-to-Test Workflow (Automated Resolution)
*   **Inputs:** User-provided bug report or error log.
*   **Outputs:** AI-generated failing test, AI-generated code fix, execution logs, and resolution diff.

### Module 4: Active Security & Threat Mitigation Agent (Parallel Sub-Project)
*   **Team Allocation:** This specific module is being developed in parallel by an independent sub-team of 2 developers.
*   **Role:** An autonomous background agent running on the server to ensure production environment integrity.
*   **Inputs:** Real-time server logs, network traffic, SSH access logs, system resource utilization (e.g., CPU/GPU spikes indicative of mining), and file system activity.
*   **Outputs:** Automated IP blocking, connection termination, threat alert logging, and real-time security dashboard updates.
*   **Capabilities:** Continuously monitors the server and actively blocks:
    *   Brute-force attack attempts.
    *   Virus and malware signatures.
    *   Honeypot trap triggers.
    *   Unauthorized cryptomining processes.
    *   Anomalous or unauthorized SSH access attempts.

---

## 3. System Architecture & Components

### Component A: Core Django Backend (Brain & Persistence)
*   **Role:** Central orchestrator handling HTTP requests, database transactions, and triggering AI/subprocess workflows.
*   **Key Models:**
    *   `ProjectContext`: Stores project metadata.
    *   `EvaluationReport`: Stores JSON/text outputs of Venture/Ship audits.
    *   `BugTicket`: Stores customer complaints, generated test code, generated fixes, and state.
    *   `SecurityEvent`: Logs threats intercepted by the Security Agent (Module 4).
*   **Interfaces:** Django Views/DRF endpoints to accept input and serve HTMX fragments.

### Component B: Python MCP Server (AI Bridge)
*   **Role:** Acts as the communication bridge between the Django application and IBM Bob using the Model Context Protocol.
*   **Registered Tools:**
    *   `audit_project`: Extracts project files/goals from Django, passes them to Bob for critique.
    *   `read_bug_and_locate`: Passes bug descriptions to Bob to identify target files.

### Component C: Bug-to-Test Execution Engine (Sandbox)
*   **Role:** Local code execution environment managed by Python.
*   **Workflow:** Prompts Bob for a test file -> executes via `subprocess` -> captures logs -> prompts Bob for fix -> re-runs test.

### Component D: Frontend / Proxy Layer
*   **Role:** User interaction and network routing. Nginx routes traffic, while HTMX dynamically updates UI components based on the database state.

### Component E: Autonomous Security Daemon
*   **Role:** The standalone monitoring service managed by the 2-person sub-team. It runs parallel to the web application, actively parsing system logs and managing firewall rules (e.g., iptables/ufw) to block detected threats in real-time.

---

## 4. Primary Data Flow: Bug-to-Test Execution Loop

1.  **Ingestion:** User submits a bug report via the Django UI ("App crashes on empty cart").
2.  **State Initialization:** Django creates a `BugTicket` in MySQL with `status = analyzing`.
3.  **AI Contextualization:** Django triggers the Python MCP client, handing the bug text and project context to IBM Bob.
4.  **Test Generation:** IBM Bob generates a test script to reproduce the bug. Django writes this script to the execution sandbox.
5.  **Execution (Validation of Failure):** Component C runs the test via `subprocess`. It captures the expected failure stack trace.
6.  **State Update 1:** MySQL `BugTicket` status updates to `test_failed`. HTMX dynamically updates the UI to show a Red "Test Failing" alert.
7.  **Fix Generation:** Python MCP client sends the captured stack trace to IBM Bob. Bob generates the code patch.
8.  **Execution (Validation of Fix):** Component C applies the patch and re-runs the test via `subprocess`. The test passes.
9.  **State Update 2:** MySQL `BugTicket` status updates to `fixed`.
10. **Resolution Delivery:** HTMX dynamically updates the UI to a Green "Bug Fixed