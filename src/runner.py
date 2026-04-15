import json
from pathlib import Path

from llm import ask_model
from planner import QA_SYSTEM_PROMPT
from tools.api_checks import run_api_check
from tools.browser_checks import check_homepage
from tools.load_checks import run_k6

def main():
    run_input = json.loads(Path("runs/sample_run.json").read_text())
    context = Path(run_input["project_context_path"]).read_text()

    user_prompt = f"""
Project name: {run_input['project_name']}

Project context:
{context}

Environment:
{json.dumps(run_input['environment'], indent=2)}

Scope:
{json.dumps(run_input['scope'], indent=2)}

Allowed actions:
{json.dumps(run_input['allowed_actions'], indent=2)}
"""

    print("\\n=== GENERATING TEST PLAN ===\\n")
    plan = ask_model(QA_SYSTEM_PROMPT, user_prompt)
    print(plan)

    print("\\n=== RUNNING API CHECK ===\\n")
    api_result = run_api_check(run_input["environment"]["api_base_url"], "/health")
    print(api_result)

    print("\\n=== RUNNING BROWSER CHECK ===\\n")
    browser_result = check_homepage(run_input["environment"]["ui_base_url"])
    print(browser_result)

    print("\\n=== RUNNING LOAD CHECK ===\\n")
    load_result = run_k6("k6/smoke.js")
    print(load_result)

    Path("reports").mkdir(exist_ok=True)
    report = (
    "# QA Run Report\n\n"
    "## Test Plan\n```json\n"
    + plan
    + "\n```\n\n"
    "## API Check\n" + str(api_result) + "\n\n"
    "## Browser Check\n" + str(browser_result) + "\n\n"
    "## Load Check\n" + str(load_result) + "\n"
    )
    Path("reports/latest_report.md").write_text(report)
