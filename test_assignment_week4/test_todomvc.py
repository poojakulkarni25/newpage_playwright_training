from playwright.sync_api import expect

from .config import Config
from .todo_page import TodoPage


def test_add_todo(page):
    page_object = TodoPage(page, Config.BASE_URL)
    page_object.goto()
    page_object.add_todo("Task Add")

    expect(page_object.get_todo_label(0)).to_contain_text("Task Add")


def test_complete_todo(page):
    page_object = TodoPage(page, Config.BASE_URL)
    page_object.goto()
    page_object.add_todo("A")
    page_object.add_todo("B")

    expect(page.locator(page_object.TODO_ITEMS)).to_have_count(2)

    page_object.complete_todo_at(0)

    expect(page.locator(f"{page_object.TODO_ITEMS}.completed")).to_have_count(1)
    expect(page.locator(page_object.TODO_COUNT)).to_have_text("1")


def test_delete_todo(page):
    page_object = TodoPage(page, Config.BASE_URL)
    page_object.goto()
    page_object.add_todo("ToDelete")

    page_object.delete_todo_at(0)

    expect(page.locator(page_object.TODO_ITEMS)).to_have_count(0)


def test_filter_todos(page):
    page_object = TodoPage(page, Config.BASE_URL)
    page_object.goto()
    page_object.add_todo("t1")
    page_object.add_todo("t2")
    page_object.add_todo("t3")

    page_object.complete_todo_at(1)
    page_object.filter_active()

    expect(page.locator(f"{page_object.TODO_ITEMS}:not(.completed)"), "2 active items expected").to_have_count(2)


def test_edit_todo(page):
    page_object = TodoPage(page, Config.BASE_URL)
    page_object.goto()
    page_object.add_todo("Old Text")

    page_object.edit_todo_at(0, "New Text")

    expect(page_object.get_todo_label(0)).to_contain_text("New Text")


def test_add_five_dynamic_todos_from_faker(page, dynamic_todo_items):
    page_object = TodoPage(page, Config.BASE_URL)
    page_object.goto()

    for todo_text in dynamic_todo_items:
        page_object.add_todo(todo_text)

    expect(page.locator(page_object.TODO_ITEMS)).to_have_count(5)
    for index, todo_text in enumerate(dynamic_todo_items):
        expect(page_object.get_todo_label(index)).to_contain_text(todo_text)


def test_add_static_todos_from_json_fixture(page, static_todo_data):
    page_object = TodoPage(page, Config.BASE_URL)
    page_object.goto()

    for todo_text in static_todo_data:
        page_object.add_todo( todo_text)

    expect(page.locator(page_object.TODO_ITEMS)).to_have_count(len(static_todo_data))
    for index, todo_text in enumerate(static_todo_data):
        expect(page_object.get_todo_label(index)).to_contain_text(todo_text)
