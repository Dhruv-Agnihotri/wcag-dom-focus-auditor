from fastapi import FastAPI
from pydantic import BaseModel, HttpUrl
from playwright.sync_api import sync_playwright
from app.dom_scanner import AccessibilityViolation, scan_dom_accessibility
from app.focus_verifier import verify_keyboard_focus_visible

app = FastAPI(title="WCAG 2.1 DOM & Focus Auditor", version="1.0.0")


class AuditRequest(BaseModel):
    url: HttpUrl


class AuditResponse(BaseModel):
    url: str
    violation_count: int
    violations: list[AccessibilityViolation]
    focus_check: dict


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/audit", response_model=AuditResponse)
def audit_url(payload: AuditRequest) -> AuditResponse:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(str(payload.url), wait_until="domcontentloaded")
        violations = scan_dom_accessibility(page)
        focus_check = verify_keyboard_focus_visible(page)
        browser.close()

    return AuditResponse(
        url=str(payload.url),
        violation_count=len(violations),
        violations=violations,
        focus_check=focus_check,
    )
