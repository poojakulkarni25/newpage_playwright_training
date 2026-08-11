import pytest
from playwright.sync_api import expect


URL = "https://demo.playwright.dev/todomvc"


def add_todo(page, text: str):
    input_locator = page.locator("input.new-todo")
    input_locator.fill(text)
    input_locator.press("Enter")
    # Wait for the item to appear in the list
    page.wait_for_selector("ul.todo-list li", timeout=5000)


def get_todo_label(page, index=0):
    return page.locator("ul.todo-list li").nth(index).locator("label")


def test_add_todo(page):
    """Test 1 — Add Todo: add a new todo and assert it appears in the list."""
    page.goto(URL)
    add_todo(page, "Task Add")

    # Explicit expect assertion for the label text
    label = get_todo_label(page, 0)
    expect(label).to_contain_text("Task Add")


def test_complete_todo(page):
    """Test 2 — Complete Todo: add two todos, complete one, assert completed and active count."""
    page.goto(URL)
    # Add two items
    add_todo(page, "A")
    add_todo(page, "B")

    # Ensure two active todos initially
    expect(page.locator("ul.todo-list li")).to_have_count(2)

    # Complete the first todo
    first = page.locator("ul.todo-list li").first
    first.locator("input.toggle").check()

    # Wait and assert there is one completed and active count is 1
    expect(page.locator("ul.todo-list li.completed")).to_have_count(1)
    expect(page.locator("span.todo-count strong")).to_have_text("1")


def test_delete_todo(page):
    """Test 3 — Delete Todo: add a todo, hover to reveal delete, click, assert empty list."""
    page.goto(URL)
    add_todo(page, "ToDelete")

    item = page.locator("ul.todo-list li").first
    # Hover to reveal destroy button then click it
    item.hover()
    destroy = item.locator("button.destroy")
    destroy.click()

    # Assert no items remain
    expect(page.locator("ul.todo-list li")).to_have_count(0)


def test_filter_todos(page):
    """Test 4 — Filter Todos: add 3 todos, complete 1, click Active filter, assert only 2 visible."""
    page.goto(URL)
    add_todo(page, "t1")
    add_todo(page, "t2")
    add_todo(page, "t3")

    # Complete second item
    page.locator("ul.todo-list li").nth(1).locator("input.toggle").check()

    # Click 'Active' filter
    page.get_by_role("link", name="Active").click()

    # Active items are those not completed; assert two active items
    expect(page.locator("ul.todo-list li:not(.completed)"), "2 active items expected").to_have_count(2)


def test_edit_todo(page):
    """Test 5 — Edit Todo: double-click to edit, change text, press Enter, assert updated text."""
    page.goto(URL)
    add_todo(page, "Old Text")

    label = get_todo_label(page, 0)
    # Double click to enter edit mode
    label.dblclick()

    edit_input = page.locator("ul.todo-list li").first.locator("input.edit")
    expect(edit_input).to_be_visible()
    edit_input.fill("New Text")
    edit_input.press("Enter")

    # Assert the label now contains the updated text
    expect(get_todo_label(page, 0)).to_contain_text("New Text")
