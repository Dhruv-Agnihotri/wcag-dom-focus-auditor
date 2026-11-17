import cv2
import numpy as np
from playwright.sync_api import Page


def verify_keyboard_focus_visible(page: Page, min_changed_pixels: int = 25) -> dict:
    """
    Presses Tab and uses OpenCV pixel differencing to verify that a visible
    focus ring renders on the focused control (WCAG 2.4.7 Focus Visible).
    """
    before_bytes = page.screenshot()
    page.keyboard.press("Tab")
    after_bytes = page.screenshot()

    img_before = cv2.imdecode(np.frombuffer(before_bytes, np.uint8), cv2.IMREAD_COLOR)
    img_after = cv2.imdecode(np.frombuffer(after_bytes, np.uint8), cv2.IMREAD_COLOR)

    diff = cv2.absdiff(img_before, img_after)
    gray_diff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    changed_pixels = int(np.count_nonzero(gray_diff > 15))

    active_tag = page.evaluate("() => document.activeElement ? document.activeElement.tagName : 'NONE'")
    return {
        "active_element": active_tag,
        "changed_pixels": changed_pixels,
        "focus_indicator_visible": changed_pixels >= min_changed_pixels,
    }
