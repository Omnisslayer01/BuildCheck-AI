# BuildCheck AI - Bug-to-Test Workflow Plan

**Current Status:** Django Project (`BuildCheck_AI`) and App (`testing`) created.
**Prerequisites:** Ensure you run `pip install pytest mcp requests` in your terminal before starting.

---

## Step 1: The Bug Tracking Database (Django Models)
**Goal:** Create a database table to store the bug reports and their live status so your future web dashboard can display them.

* **Prompt for Bob:**
  > "@testing/models.py @testing/admin.py Create a Django model named `BugTicket`. 
  > It should have fields: `title` (CharField), `bug_description` (TextField), `status` (CharField with choices: 'analyzing', 'test_failed', 'fixed', default='analyzing'), and `created_at` (DateTimeField auto_now_add). 
  > In `admin.py`, register this model so I can view and edit it in the Django Admin panel."

* **Test & Validate:**
  1. In your terminal: `python manage.py makemigrations`
  2. Then: `python manage.py migrate`
  3. Create an admin account: `python manage.py createsuperuser`
  4. Run the server: `python manage.py runserver`
  5. Go to `http://127.0.0.1:8000/admin` in your browser. Log in. Do you see "Bug Tickets"? If yes, Success!
  6. *Commit:* `git add . && git commit -m "Step 1: BugTicket Model"`

---

## Step 2: The Status Webhook (Django API)
**Goal:** Create a hidden URL. Later, your Python Sandbox will send a message here to automatically change a bug's status from "failed" to "fixed".

* **Prompt for Bob:**
  > "@testing/views.py @testing/urls.py Create a JSON API endpoint.
  > Create a view called `update_bug_status` that accepts a POST request. It should expect JSON like `{"ticket_id": 1, "status": "fixed"}`. It should find the `BugTicket` with that ID and update its status. Return a JSON success message.
  > Use the `@csrf_exempt` decorator on the view so our external sandbox script can post to it easily. Wire it up to a URL path `/api/update-status/`."

* **Test & Validate:**
  1. Create a dummy `BugTicket` in your Django Admin panel (Note its ID, usually 1).
  2. Open a *new* terminal window.
  3. Test the API using cURL (replace `1` with your ticket ID if different):
     `curl -X POST http://127.0.0.1:8000/api/update-status/ -H "Content-Type: application/json" -d '{"ticket_id": 1, "status": "fixed"}'`
  4. Go back to Django Admin and refresh. Did the status change to "fixed"? If yes, Success!
  5. *Commit:* `git add . && git commit -m "Step 2: Status Webhook API"`

---

## Step 3: The "Dummy App" & Bug Report
**Goal:** Create a broken piece of code and a customer complaint so IBM Bob has something to test and fix during your demo.

* **Manual Step (No Bob needed):**
  1. Create a file in your main root folder called `cart.py`.
  2. Paste this intentionally broken code into it:
     ```python
     class ShoppingCart:
         def __init__(self):
             self.items = []

         def add_item(self, name, quantity):
             # BUG: Doesn't check for negative quantities!
             self.items.append({"name": name, "qty": quantity})
             return True

         def get_total_items(self):
             return sum(item["qty"] for item in self.items)
     ```
  3. Create a text file named `bug_report.txt` and paste this:
     ```text
     Customer Issue #992: 
     "If I type -5 into the quantity box, the cart accepts it and subtracts from my total! It should throw a ValueError if the quantity is less than 1."
     ```
  4. *Commit:* `git add . && git commit -m "Step 3: Dummy App Setup"`

---

## Step 4: The Execution Sandbox
**Goal:** Create the Python script that will actually run the `pytest` tests that Bob generates.

* **Prompt for Bob:**
  > "Create a new file in the root directory called `sandbox.py`. 
  > Write a function `run_generated_test(test_code_string)`. 
  > 1. It should write the `test_code_string` to a file called `temp_test_cart.py`.
  > 2. Use the `subprocess` module to run `pytest temp_test_cart.py`.
  > 3. Capture both `stdout` and `stderr`.
  > 4. Delete `temp_test_cart.py` after running.
  > 5. Return a string containing the captured terminal output so the LLM can read why it failed or passed."

* **Test & Validate:**
  1. Open your terminal and run the Python shell: `python`
  2. Type: `from sandbox import run_generated_test`
  3. Type: `print(run_generated_test("def test_math(): assert 1 == 2"))`
  4. Did it print out a pytest failure message? If yes, the sandbox works!
  5. Type `exit()` to leave the shell.
  6. *Commit:* `git add . && git commit -m "Step 4: Sandbox execution"`

---

## Step 5: The IBM Bob MCP Server (The Magic Bridge)
**Goal:** Connect IBM Bob to your Sandbox so Bob can execute tests by himself.

* **Prompt for Bob:**
  > "@sandbox.py Create a new file called `mcp_server.py`. 
  > Using the official Python `mcp` library (`from mcp.server.fastmcp import FastMCP`), initialize an MCP server.
  > Create an `@mcp.tool()` called `execute_pytest`. This tool should accept a string argument `test_code_string`. Inside the tool, call `sandbox.py`'s `run_generated_test` function, and return the terminal output.
  > Add the `mcp.run()` command at the bottom so the server can start."

* **Test & Validate:**
  1. In the IBM Bob IDE, click the **Settings Icon (gear)**.
  2. Go to **MCP Servers** -> **Add Local Server** (or edit the `mcp.json` config).
  3. Configure it to run your script. Example config:
     * Command: `python` (or the absolute path to your venv python, e.g., `C:/.../venv/Scripts/python.exe`)
     * Arguments: `mcp_server.py`
  4. Restart IBM Bob or refresh the MCP connection.
  5. Open the Bob Chat and ask: *"List your available tools."* Do you see `execute_pytest`? If yes, Success!
  6. *Commit:* `git add . && git commit -m "Step 5: MCP Server Online"`

---

## Step 6: The Final Demo Run!
**Goal:** Trigger the automated Bug-to-Test loop. Make sure your MCP server is connected.

* **Prompt for Bob (The ultimate test):**
  > "@bug_report.txt @cart.py Read the bug report. 
  > 1. Write a pytest function to replicate the bug described. 
  > 2. Use your `execute_pytest` tool to run the test. It should fail.
  > 3. Read the failure output, then fix `cart.py` to resolve the bug.
  > 4. Use the `execute_pytest` tool a second time to verify your fix works."

* **Test & Validate:**
  Watch Bob go to work. It should generate the test, run it, see the failure, fix the `add_item` logic in `cart.py`, run it again, and report success.

Once you have written and saved the code, open @PROGRESS.md. Write a heading for this Step, mark it as [COMPLETED], and write a 2-sentence summary of the exact files you modified, the functions you created, and how they solve this step. This will serve as context for our next step