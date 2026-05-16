# BuildCheck AI - Dashboard & Grand Finale Plan

**Current Status:** The Bug-to-Test MCP Engine is fully operational.
**Goal:** Build the live-updating Web Dashboard to visualize the AI's autonomous work, and run the final end-to-end demo.

---

## Step 1: The Manager's Dashboard (UI Template)
**Goal:** Create a beautiful, dark-mode web page that lists all the bugs currently in the database.

* **Prompt for Bob:**
  > "@testing/views.py @testing/urls.py I need to build the main web dashboard. 
  > 1. In `views.py`, create a new view called `dashboard` that fetches all `BugTicket` objects and renders `dashboard.html`.
  > 2. In `urls.py`, wire this view to the root URL `path('', views.dashboard, name='dashboard')`.
  > 3. Create a new file at `testing/templates/dashboard.html`. Write a complete HTML5 document. Use TailwindCSS via CDN (`<script src="https://cdn.tailwindcss.com"></script>`). 
  > 4. Design it as a sleek, dark-mode developer dashboard. Add a header "BuildCheck AI Command Center". Below that, create a stylized table listing all Bug Tickets (ID, Title, Description, Status). 
  > 5. Style the Status column as badges: Green for 'fixed', Red for 'test_failed', and Yellow for 'analyzing'.

* **Test & Validate:**
  1. Make sure your Django server is running: `python manage.py runserver`
  2. Open `http://127.0.0.1:8000/` in your browser.
  3. Do you see a dark-themed dashboard with your test bugs? If yes, Success!
  4. *Commit:* `git add . && git commit -m "Dashboard UI created"`

---

## Step 2: Auto-Refreshing the UI (HTMX Magic)
**Goal:** Make the dashboard automatically update itself every 3 seconds so you don't have to click "Refresh" during your demo.

* **Prompt for Bob:**
  > "@testing/templates/dashboard.html @testing/views.py @testing/urls.py We need to make the dashboard table auto-refresh using HTMX.
  > 1. In `dashboard.html`, add the HTMX script to the `<head>`: `<script src="https://unpkg.com/htmx.org@1.9.10"></script>`.
  > 2. Extract the `<tbody>` (the rows of the bug table) into a new file called `testing/templates/bug_table_rows.html`. 
  > 3. In `dashboard.html`, replace the table body with a `<tbody>` that uses HTMX to poll for updates: `<tbody hx-get="/api/bug-list-html/" hx-trigger="every 3s" hx-swap="innerHTML"> {% include 'bug_table_rows.html' %} </tbody>`.
  > 4. In `views.py`, create a new view `bug_list_html` that fetches all `BugTicket` objects and renders ONLY `bug_table_rows.html`.
  > 5. In `urls.py`, route `/api/bug-list-html/` to this new view."

* **Test & Validate:**
  1. Keep your dashboard open in one browser window.
  2. Open a new tab and go to the Django Admin (`http://127.0.0.1:8000/admin`).
  3. Change the status of a BugTicket in the Admin panel and click Save.
  4. Look back at your dashboard window. Did the color badge change automatically within 3 seconds? If yes, HTMX is working!
  5. *Commit:* `git add . && git commit -m "HTMX auto-refresh implemented"`

---

## Step 3: The Grand Finale (End-to-End Demo)
**Goal:** Run the entire system from start to finish. This is what you will record for your hackathon video!

* **Manual Setup (Resetting the Trap):**
  1. Open `cart.py`. Remove the negative number validation. Make the code broken again.
  2. Go to Django Admin. Change the status of your BugTicket back to `analyzing`. 
  3. **Note the ID** of that BugTicket (e.g., ID: 1).

* **The Setup for the Video:**
  1. Arrange your screen: Put the **Web Dashboard** on the left half of your screen. Put **IBM Bob / VS Code** on the right half.
  2. Start your screen recording.

* **Prompt for Bob (The Magic Command):**
  > "@bug_report.txt @cart.py The ticket ID for this bug is 1. 
  > Please execute the Bug-to-Test workflow autonomously:
  > 1. Use `write_file` to create a pytest that replicates the bug.
  > 2. Use `run_test` to verify the test fails.
  > 3. Fix `cart.py` to handle negative quantities.
  > 4. Use `run_test` again to verify the test passes.
  > 5. Once verified, use `report_to_boss` to change ticket 1 to 'fixed'."

* **Watch the Magic:**
  1. Bob will generate the test.
  2. Bob will call the Sandbox (Tool call).
  3. Bob will fix the code.
  4. Bob will call the Sandbox again.
  5. Bob will call the Webhook API.
  6. **On the left side of your screen, your web dashboard will magically update from RED to GREEN.**

---

## Step 4: The Most Important Step (Exporting the Log)
**Goal:** Secure your hackathon submission.

1. Once Bob finishes the Grand Finale, click the `...` menu at the top of the Bob Chat.
2. Select **History**.
3. Click on the chat session you just completed.
4. Take a **Screenshot** of the consumption summary box.
5. Click the **Export icon** to download the Markdown file of this conversation.
6. Put BOTH the screenshot and the Markdown file into a folder named `bob_sessions` inside your project.
7. *Commit and Push to GitHub!*