from playwright.sync_api import sync_playwright

URL = "https://demo.playwright.dev/todomvc"


def main() -> None:
    todo_items = ["Buy groceries", "Write tests", "Walk the dog"]

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page(viewport={"width": 1280, "height": 900})
        page.goto(URL, wait_until="networkidle", timeout=60000)

        new_todo = page.locator("input.new-todo")
        for item in todo_items:
            new_todo.fill(item)
            new_todo.press("Enter")
            # Wait 3 seconds after adding an item to allow UI updates
            page.wait_for_timeout(3000)

        todo_rows = page.locator("ul.todo-list li")
        assert todo_rows.count() == 3, "Expected 3 todo items after creation"

        # Complete the first two todos
        for index in range(2):
            todo_rows.nth(index).locator("input.toggle").check()
            # Wait 3 seconds after completing an item to allow UI updates
            page.wait_for_timeout(3000)

        completed_rows = page.locator("ul.todo-list li.completed")
        assert completed_rows.count() == 2, "Expected 2 completed todos"

        clear_button = page.get_by_role("button", name="Clear completed")
        clear_button.click()
        # Wait 3 seconds after clearing completed items to allow UI updates
        page.wait_for_timeout(3000)

        # After clearing completed todos, only one active item should remain
        remaining_rows = page.locator("ul.todo-list li")
        assert remaining_rows.count() == 1, "Expected 1 remaining todo after clearing completed items"

        remaining_count = page.locator("span.todo-count strong").text_content()
        assert remaining_count == "1", f"Expected remaining count to be 1, got {remaining_count}"
        remaining_text = page.locator("span.todo-count").text_content()
        assert "1 item left" in remaining_text, f"Expected text '1 item left', got {remaining_text}"

        print("TodoMVC flow completed successfully")

        browser.close()


if __name__ == "__main__":
    main()
