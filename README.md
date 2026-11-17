# WCAG 2.1 DOM & Computer-Vision Focus Auditor

![CI Status](https://img.shields.io/badge/CI-GitHub_Actions-2088FF?logo=github-actions&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.111+-009688?logo=fastapi&logoColor=white)
![Playwright](https://img.shields.io/badge/Playwright-DOM_Audit-45ba4b?logo=playwright&logoColor=white)
![OpenCV](https://img.shields.io/badge/OpenCV-Focus_Ring_CV-5C3EE8?logo=opencv&logoColor=white)

An automated accessibility auditing service combining **Playwright DOM inspection** with **OpenCV visual focus-ring verification** and a **FastAPI REST API**.

## Capabilities
1. **WCAG 2.1 DOM Scanner (`app/dom_scanner.py`):**
   - **WCAG 1.1.1:** Flags `<img>` elements missing `alt` attributes.
   - **WCAG 3.3.2 / 4.1.2:** Flags form `<input>` controls lacking `<label>`, `aria-label`, or `aria-labelledby`.
   - **WCAG 3.1.1:** Verifies `<html>` declares a valid `lang` attribute.
   - **WCAG 2.4.4:** Detects empty links (`<a>` with no accessible name).
2. **Computer-Vision Focus Indicator Verifier (`app/focus_verifier.py`):**
   - Simulates keyboard `Tab` navigation across interactive controls and compares before/after screenshots via **OpenCV pixel-delta analysis** to verify visible focus rings (WCAG 2.4.7).
3. **FastAPI Service (`app/main.py`):**
   - Exposes `POST /audit` returning structured WCAG violation JSON ready for CI gates or LLM remediation prompts.

## Quickstart

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
playwright install chromium

# Run unit & integration tests
pytest -v

# Start FastAPI server
uvicorn app.main:app --reload
```
