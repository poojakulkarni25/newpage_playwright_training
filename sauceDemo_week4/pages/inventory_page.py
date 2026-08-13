from pages.base_page import BasePage


class InventoryPage(BasePage):
    INVENTORY_LIST = ".inventory_list"
    ADD_TO_CART_BUTTON = "button.btn_inventory"
    CART_BADGE = ".shopping_cart_badge"

    def is_loaded(self) -> bool:
        return self.is_visible(self.INVENTORY_LIST)

    def add_first_item_to_cart(self) -> None:
        self.click(self.ADD_TO_CART_BUTTON)
        self.wait_for_selector(self.CART_BADGE)

    def get_cart_count(self) -> int:
        if self.is_visible(self.CART_BADGE):
            return int(self.text_content(self.CART_BADGE).strip())
        return 0
