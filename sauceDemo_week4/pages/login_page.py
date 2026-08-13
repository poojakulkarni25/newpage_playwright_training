from playwright.sync_api import Page

from config import Config
from pages.base_page import BasePage
from pages.inventory_page import InventoryPage


class LoginPage(BasePage):
    USERNAME_INPUT = "#user-name"
    PASSWORD_INPUT = "#password"
    LOGIN_BUTTON = "#login-button"
    ERROR_MESSAGE = "[data-test=error]"

    def load(self) -> None:
        self.goto(Config.BASE_URL)
        self.wait_for_selector(self.USERNAME_INPUT)

    def login(self, username: str, password: str) -> InventoryPage:
        self.fill(self.USERNAME_INPUT, username)
        self.fill(self.PASSWORD_INPUT, password)
        self.click(self.LOGIN_BUTTON)
        return InventoryPage(self.page)

    def get_error_message(self) -> str:
        if self.is_visible(self.ERROR_MESSAGE):
            return self.text_content(self.ERROR_MESSAGE).strip()
        return ""
