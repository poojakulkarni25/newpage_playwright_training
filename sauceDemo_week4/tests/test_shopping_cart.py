from config import Config
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage


def test_add_item_to_cart_updates_badge(page):
    login_page = LoginPage(page)
    login_page.load()

    inventory_page = login_page.login(Config.USERNAME, Config.PASSWORD)
    assert inventory_page.is_loaded(), "Inventory should be visible after login"

    inventory_page.add_first_item_to_cart()

    assert inventory_page.get_cart_count() == 1, "Cart badge should display 1 item after adding one product"
