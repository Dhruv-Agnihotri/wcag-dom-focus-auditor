from fastapi.testclient import TestClient
from playwright.sync_api import sync_playwright
from app.dom_scanner import scan_dom_accessibility
from app.focus_verifier import verify_keyboard_focus_visible
from app.main import app


def test_health_endpoint():
    client = TestClient(app)
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}


def test_dom_scanner_and_focus_ring_detection():
    sample_html = """
    <html>
      <body>
        <img src="banner.png">
        <form><input type="text" name="email"></form>
        <button id="submit-btn" style="margin:20px; padding:10px;">Submit</button>
      </body>
    </html>
    """
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.set_content(sample_html)

        violations = scan_dom_accessibility(page)
        rule_ids = {v.rule_id for v in violations}
        assert "html-has-lang" in rule_ids
        assert "image-alt" in rule_ids
        assert "label" in rule_ids

        focus_result = verify_keyboard_focus_visible(page)
        assert focus_result["active_element"] == "BUTTON"
        assert focus_result["focus_indicator_visible"] is True
        browser.close()
