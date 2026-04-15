import httpx

def run_api_check(base_url: str, path: str, expected_status: int = 200) -> dict:
    url = base_url.rstrip("/") + path
    with httpx.Client(timeout=20.0) as client:
        response = client.get(url)

    return {
        "tool": "api_check",
        "url": url,
        "status_code": response.status_code,
        "ok": response.status_code == expected_status,
        "body_preview": response.text[:500],
    }