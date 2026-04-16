from pathlib import Path
import sys

sys.path.append("src")

import runner


def test_runner_creates_report(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)

    # recreate minimal project structure inside temp folder
    Path("runs").mkdir()
    Path("context").mkdir()
    Path("reports").mkdir()
    Path("k6").mkdir()

    Path("context/project_context.md").write_text(
        "# Test Project Context\nThis is a test context file.",
        encoding="utf-8"
    )

    Path("runs/sample_run.json").write_text(
        """
{
  "project_name": "QA in a Box",
  "project_context_path": "context/project_context.md",
  "environment": {
    "api_base_url": "http://localhost:8000",
    "ui_base_url": "http://localhost:3000",
    "env_name": "local"
  },
  "credentials": {
    "api_keys": [],
    "users": []
  },
  "scope": {
    "endpoints": ["/health"],
    "pages": ["/"],
    "excluded_paths": []
  },
  "allowed_actions": {
    "browser_testing": true,
    "api_testing": true,
    "load_testing": true,
    "data_mutation": false
  },
  "success_criteria": {
    "p95_ms": 800,
    "error_rate_pct": 1
  }
}
""",
        encoding="utf-8"
    )

    # mock external dependencies
    monkeypatch.setattr(
        runner,
        "ask_model",
        lambda system_prompt, user_prompt: '{"test_plan":[{"id":"T1","type":"api","title":"Health check","objective":"Verify /health","steps":["Call /health"],"expected_result":"200 OK","severity_if_fail":"high"}]}'
    )

    monkeypatch.setattr(
        runner,
        "run_api_check",
        lambda base_url, path: {
            "tool": "api_check",
            "url": f"{base_url}{path}",
            "status_code": 200,
            "ok": True,
            "body_preview": '{"status":"ok"}'
        }
    )

    monkeypatch.setattr(
        runner,
        "check_homepage",
        lambda url: {
            "tool": "browser_check",
            "url": url,
            "title": "Test Home",
            "screenshot": "artifacts/homepage.png"
        }
    )

    monkeypatch.setattr(
        runner,
        "run_k6",
        lambda script_path: {
            "tool": "load_check",
            "ok": True,
            "stdout": "k6 run passed",
            "stderr": ""
        }
    )

    runner.main()

    report_path = Path("reports/latest_report.md")
    assert report_path.exists()

    content = report_path.read_text(encoding="utf-8")
    assert "# QA Run Report" in content
    assert "## API Check" in content
    assert "## Browser Check" in content
    assert "## Load Check" in content