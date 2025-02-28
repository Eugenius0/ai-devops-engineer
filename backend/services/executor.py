import subprocess
from pathlib import Path
import sys

BASE_DIR = Path(__file__).resolve().parent.parent.parent
SCRIPTS_DIR = BASE_DIR / "automation_scripts"

def run_script(script_name, repo_name):
    """Runs an automation script and streams its output."""
    script_path = SCRIPTS_DIR / script_name

    if not script_path.exists():
        yield f"Error: Script {script_name} not found at {script_path}"
        return

    process = subprocess.Popen(
        ["python", "-u", str(script_path), repo_name], 
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, bufsize=1, universal_newlines=True
    )

    # Stream standard output in real-time
    for line in iter(process.stdout.readline, ''):
        sys.stdout.write(line)
        sys.stdout.flush()  # 🔄 Force immediate output
        yield line  # 🔥 Stream line to FastAPI

    # Stream errors separately in real-time
    for err_line in iter(process.stderr.readline, ''):
        sys.stderr.write(err_line)
        sys.stderr.flush()
        yield f"ERROR: {err_line}"

    process.stdout.close()
    process.stderr.close()
    process.wait()
