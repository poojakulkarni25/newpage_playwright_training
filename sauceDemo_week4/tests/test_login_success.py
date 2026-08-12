from config import Config
from pages.login_page import LoginPage


def test_successful_login(page):
    login_page = LoginPage(page)
    login_page.load()

    inventory_page = login_page.login(Config.USERNAME, Config.PASSWORD)

    assert inventory_page.is_loaded(), "Expected inventory page to load after successful login"
