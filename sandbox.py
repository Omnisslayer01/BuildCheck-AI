import subprocess
import os


def run_generated_test(test_code_string):
    """
    Execute a pytest test from a code string.
    
    Args:
        test_code_string: Python test code as a string
        
    Returns:
        String containing the captured terminal output (stdout and stderr)
    """
    test_file = "temp_test_cart.py"
    
    try:
        # Step 1: Write the test code to a temporary file
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write(test_code_string)
        
        # Step 2: Run pytest on the temporary file
        result = subprocess.run(
            ["pytest", test_file, "-v"],
            capture_output=True,
            text=True
        )
        
        # Step 3: Capture both stdout and stderr
        output = f"=== PYTEST OUTPUT ===\n"
        output += f"Return Code: {result.returncode}\n\n"
        
        if result.stdout:
            output += f"STDOUT:\n{result.stdout}\n"
        
        if result.stderr:
            output += f"STDERR:\n{result.stderr}\n"
        
        return output
        
    except FileNotFoundError:
        return "Error: pytest is not installed or not found in PATH. Please run: pip install pytest"
    
    except Exception as e:
        return f"Error running test: {str(e)}"
    
    finally:
        # Step 4: Delete the temporary test file
        if os.path.exists(test_file):
            try:
                os.remove(test_file)
            except Exception as e:
                print(f"Warning: Could not delete {test_file}: {e}")


if __name__ == "__main__":
    # Example usage for testing
    test_code = """
def test_math():
    assert 1 == 2
"""
    print(run_generated_test(test_code))

# Made with Bob
