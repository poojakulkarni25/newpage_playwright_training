from playwright.sync_api import Page, expect


class TodoPage:
    NEW_TODO_INPUT = "input.new-todo"
    TODO_LIST = "ul.todo-list"
    TODO_ITEMS = f"{TODO_LIST} li"
    STEP_DELAY_MS = 2000
    TODO_ITEM_LABEL = "label"
    TODO_ITEM_TOGGLE = "input.toggle"
    TODO_ITEM_DESTROY = "button.destroy"
    TODO_ITEM_EDIT = "input.edit"
    TODO_COUNT = "span.todo-count strong"
    ACTIVE_FILTER = "Active"

    def __init__(self, page: Page, base_url: str):
        self.page = page
        self.base_url = base_url

    def goto(self) -> None:
        self.page.goto(self.base_url)
        self.page.wait_for_timeout(self.STEP_DELAY_MS)

    def add_todo(self, text: str) -> None:
        input_box = self.page.locator(self.NEW_TODO_INPUT)
        input_box.fill(text)
        self.page.wait_for_timeout(self.STEP_DELAY_MS)
        input_box.press("Enter")
        self.page.wait_for_timeout(self.STEP_DELAY_MS)
        self.page.wait_for_selector(self.TODO_ITEMS, timeout=5000)

    def get_todo_label(self, index: int = 0):
        return self.page.locator(self.TODO_ITEMS).nth(index).locator(self.TODO_ITEM_LABEL)

    def todo_count(self) -> int:
        return self.page.locator(self.TODO_ITEMS).count()

    def completed_todo_count(self) -> int:
        return self.page.locator(f"{self.TODO_ITEMS}.completed").count()

    def complete_todo_at(self, index: int) -> None:
        self.page.locator(self.TODO_ITEMS).nth(index).locator(self.TODO_ITEM_TOGGLE).check()
        self.page.wait_for_timeout(self.STEP_DELAY_MS)

    def delete_todo_at(self, index: int) -> None:
        item = self.page.locator(self.TODO_ITEMS).nth(index)
        item.hover()
        self.page.wait_for_timeout(self.STEP_DELAY_MS)
        item.locator(self.TODO_ITEM_DESTROY).click()
        self.page.wait_for_timeout(self.STEP_DELAY_MS)

    def filter_active(self) -> None:
        self.page.get_by_role("link", name=self.ACTIVE_FILTER).click()
        self.page.wait_for_timeout(self.STEP_DELAY_MS)

    def edit_todo_at(self, index: int, new_text: str) -> None:
        self.get_todo_label(index).dblclick()
        self.page.wait_for_timeout(self.STEP_DELAY_MS)
        edit_input = self.page.locator(self.TODO_ITEMS).nth(index).locator(self.TODO_ITEM_EDIT)
        expect(edit_input).to_be_visible()
        edit_input.fill(new_text)
        self.page.wait_for_timeout(self.STEP_DELAY_MS)
        edit_input.press("Enter")
        self.page.wait_for_timeout(self.STEP_DELAY_MS)
