from pydantic import BaseModel
from playwright.sync_api import Page


class AccessibilityViolation(BaseModel):
    rule_id: str
    wcag_criterion: str
    severity: str
    element: str
    message: str


def scan_dom_accessibility(page: Page) -> list[AccessibilityViolation]:
    """Evaluates live DOM nodes for core WCAG 2.1 Level A/AA issues."""
    raw_issues = page.evaluate(
        """() => {
            const issues = [];
            const htmlLang = document.documentElement.getAttribute('lang');
            if (!htmlLang || !htmlLang.trim()) {
                issues.push({
                    rule_id: 'html-has-lang',
                    wcag_criterion: '3.1.1',
                    severity: 'serious',
                    element: '<html>',
                    message: 'Document <html> element is missing a non-empty lang attribute.'
                });
            }

            document.querySelectorAll('img').forEach((img, idx) => {
                if (!img.hasAttribute('alt')) {
                    issues.push({
                        rule_id: 'image-alt',
                        wcag_criterion: '1.1.1',
                        severity: 'critical',
                        element: img.outerHTML.slice(0, 100),
                        message: `Image #${idx + 1} is missing an alt attribute.`
                    });
                }
            });

            document.querySelectorAll('input:not([type="hidden"])').forEach((inp, idx) => {
                const id = inp.getAttribute('id');
                const hasForLabel = id ? Boolean(document.querySelector(`label[for="${id}"]`)) : false;
                const hasWrappingLabel = Boolean(inp.closest('label'));
                const hasAria = inp.hasAttribute('aria-label') || inp.hasAttribute('aria-labelledby');
                if (!hasForLabel && !hasWrappingLabel && !hasAria) {
                    issues.push({
                        rule_id: 'label',
                        wcag_criterion: '3.3.2',
                        severity: 'critical',
                        element: inp.outerHTML.slice(0, 100),
                        message: `Form input #${idx + 1} lacks an associated label or ARIA name.`
                    });
                }
            });

            document.querySelectorAll('a[href]').forEach((a, idx) => {
                const text = (a.innerText || '').trim();
                const aria = (a.getAttribute('aria-label') || '').trim();
                if (!text && !aria) {
                    issues.push({
                        rule_id: 'link-name',
                        wcag_criterion: '2.4.4',
                        severity: 'serious',
                        element: a.outerHTML.slice(0, 100),
                        message: `Anchor #${idx + 1} has no discernible link text.`
                    });
                }
            });

            return issues;
        }"""
    )
    return [AccessibilityViolation(**item) for item in raw_issues]
