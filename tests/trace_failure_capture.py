#!/usr/bin/env python3
"""
Create a deliberate failing test that records a Playwright trace and screenshot on failure.
Saves artifacts to ./artifacts/{screenshots,traces} and prints how to open the trace with
`playwright show-trace` or `npx playwright show-trace`.
"""

import os
import sys
import time
from playwright.sync_api import sync_playwright


def run():
    root = os.path.dirname(__file__)
    artifacts_dir = os.path.join(root, "artifacts")
    screenshots_dir = os.path.join(artifacts_dir, "screenshots")
    traces_dir = os.path.join(artifacts_dir, "traces")
    os.makedirs(screenshots_dir, exist_ok=True)
    os.makedirs(traces_dir, exist_ok=True)

    trace_path = os.path.join(traces_dir, "failure_trace.zip")
    screenshot_path = os.path.join(screenshots_dir, "failure.png")

    pw = sync_playwright().start()
    browser = pw.chromium.launch(headless=True)
    context = browser.new_context()

    # Start Playwright tracing (captures screenshots, DOM snapshots and sources)
    context.tracing.start(screenshots=True, snapshots=True, sources=True)

    page = context.new_page()

    try:
        # Navigate to page under test
        page.goto("https://demo.playwright.dev/todomvc", wait_until="networkidle")
        time.sleep(1)

        # Intentionally assert an impossible condition to force failure
        heading = page.locator("h1").first
        heading_text = heading.text_content()
        print("Page h1 text:", heading_text)

        # Deliberate failing assertion
        assert "THIS_SHOULD_FAIL" in (heading_text or ""), (
            f"Deliberate failure: expected substring not found in '{heading_text}'"
        )

        # If the assertion didn't fail (unexpected), stop tracing and exit normally
        context.tracing.stop(path=trace_path)
        print("No failure occurred. Trace saved to:", trace_path)

    except Exception as exc:
        # On failure: capture screenshot and stop tracing (saving to zip)
        print("Test failed as expected:", exc)

        try:
            page.screenshot(path=screenshot_path, full_page=True)
            print("Saved screenshot:", screenshot_path)
        except Exception as e:
            print("Failed to capture screenshot:", e)

        try:
            context.tracing.stop(path=trace_path)
            print("Saved Playwright trace:", trace_path)
        except Exception as e:
            print("Failed to save trace:", e)

        # Re-raise to make the script exit with non-zero status
        raise

    finally:
        # Clean up
        try:
            page.close()
        except Exception:
            pass
        try:
            context.close()
        except Exception:
            pass
        try:
            browser.close()
        except Exception:
            pass
        try:
            pw.stop()
        except Exception:
            pass


if __name__ == "__main__":
    try:
        run()
    except Exception:
        trace_rel = "artifacts/traces/failure_trace.zip"
        print("\nArtifacts saved (relative to script):")
        print("  - artifacts/screenshots/failure.png")
        print("  - ", trace_rel)
        print("\nTo open the trace in Playwright Trace Viewer run:")
        print("  playwright show-trace ", trace_rel)
        print("or, if you prefer npm: npx playwright show-trace ", trace_rel)
        sys.exit(1)
    else:
        print("Script completed without triggering the deliberate failure.")
        sys.exit(0)
