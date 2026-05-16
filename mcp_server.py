import subprocess
import requests
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("BuildCheck-AI")


@mcp.tool()
def write_file(file_name: str, content: str) -> str:
    """Write content to a file."""
    try:
        with open(file_name, 'w', encoding='utf-8') as f:
            f.write(content)
        return f"Successfully wrote to {file_name}"
    except Exception as e:
        return f"Error writing to {file_name}: {str(e)}"


@mcp.tool()
def run_test(file_name: str) -> str:
    """Run pytest on a file."""
    try:
        result = subprocess.run(
            ["pytest", file_name],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            return f"Tests passed for {file_name}"
        else:
            return f"Tests failed for {file_name}\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
    except Exception as e:
        return f"Error running tests: {str(e)}"


@mcp.tool()
def report_to_boss(message: str) -> str:
    """Report a message to the boss via API."""
    try:
        payload = {"source": "IBM Bob", "message": message}
        response = requests.post(
            "http://localhost:8000/api/update-status/",
            json=payload
        )
        if response.status_code == 200:
            return "Successfully reported to boss"
        else:
            return f"Error reporting to boss: Status {response.status_code}, Response: {response.text}"
    except Exception as e:
        return f"Error reporting to boss: {str(e)}"

@mcp.tool()
def submit_business_lens(score: int, verdict: str) -> str:
    """IBM Bob uses this to send a Business & Monetization Evaluation to the Dashboard."""
    try:
        payload = {
            "score": score,
            "verdict": verdict
        }
        response = requests.post("http://localhost:8000/api/business-lens/", json=payload)
        if response.status_code == 200:
            return "Business evaluation successfully sent to the Dashboard!"
        else:
            return f"Error: Status {response.status_code}"
    except Exception as e:
        return f"Failed to send business evaluation: {str(e)}"


if __name__ == "__main__":
    mcp.run()

# Made with Bob
