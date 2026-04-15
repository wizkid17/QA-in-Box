import subprocess

def run_k6(script_path: str) -> dict:
    result = subprocess.run(
        ["k6", "run", script_path],
        capture_output=True,
        text=True
    )

    return {
        "tool": "load_check",
        "ok": result.returncode == 0,
        "stdout": result.stdout[-3000:],
        "stderr": result.stderr[-1000:],
    }