import re
from playwright.sync_api import Playwright, sync_playwright, expect, Page

def login(page: Page):
    page.get_by_role("link", name="Login").click()
    page.get_by_role("textbox", name="Email").fill("new_manager@gmail.com")
    page.get_by_role("textbox", name="Password").fill("String!123")
    page.get_by_role("button", name="Login").click()

    expect(page.get_by_role("banner")).to_contain_text("new_manager@gmail.com")
    
def check_lessons_page(page: Page):
    page.get_by_role("button", name="new_manager@gmail.com").click()
    page.get_by_role("link", name="Admin").click()
    
    expect(page.get_by_role("list")).to_contain_text("Lessons")

def test_lessons_access(setup_page: Page):
    login(setup_page)
    check_lessons_page(setup_page)