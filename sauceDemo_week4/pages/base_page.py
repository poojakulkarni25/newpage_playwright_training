from playwright.sync_api import Page


class BasePage:
    def __init__(self, page: Page) -> None:
        self.page = page

    def goto(self, path: str = "") -> None:
        self.page.goto(path, wait_until="load")

    def wait_for_selector(self, selector: str, timeout: int = 5000) -> None:
        self.page.wait_for_selector(selector, timeout=timeout)

    def fill(self, selector: str, value: str) -> None:
        self.page.fill(selector, value)

    def click(self, selector: str) -> None:
        self.page.click(selector)

    def text_content(self, selector: str) -> str:
        return self.page.text_content(selector) or ""

    def is_visible(self, selector: str) -> bool:
        return self.page.is_visible(selector)
