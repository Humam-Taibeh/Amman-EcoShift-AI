import subprocess
import sys

try:
    result = subprocess.run([sys.executable, "-m", "pylint", "app", "--errors-only"], capture_output=True, text=True)
    print(result.stdout)
    print(result.stderr)
except Exception as e:
    print(f"Error: {e}")
