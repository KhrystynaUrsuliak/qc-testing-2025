import re
from playwright.sync_api import Playwright, sync_playwright, expect, Page

from test_lessons_access import login, check_lessons_page

def create_lesson(page: Page, data: dict):
    page.get_by_role("button", name="Open").click()
    page.get_by_role("option", name=data["group_name"]).click()

    page.get_by_role("combobox").filter(has_text="Teacher").get_by_label("Open").click()
    page.get_by_role("option", name=data["teacher_name"]).click()

    page.get_by_role("textbox", name="Subject", exact=True).click()
    page.get_by_role("option", name=data["subject_name"]).click()

    page.get_by_role("combobox").filter(has_text="Type").get_by_label("Open").click()
    page.get_by_role("option", name=data["lesson_type"]).click()

    page.get_by_role("textbox", name="Hour").click()
    page.get_by_role("textbox", name="Hour").fill(data["hour_value"])

    page.get_by_role("button", name="Save").click()

    expect(page.locator("#root")).to_contain_text(
        f"Copy lessonEdit lessonDelete lesson{data['subject_name']}{data['lesson_type']}{data['teacher_short']}{data['hour_value']} hour"
    )


def edit_lesson(page: Page, data: dict, new_lesson_type: str):

    page.get_by_role("img", name="Edit lesson").locator("path").click()

    page.get_by_role("combobox").filter(has_text="Type").get_by_label("Open").click()
    page.get_by_role("option", name=new_lesson_type).click()
    page.get_by_role("button", name="Save").click()

    expect(page.locator("#root")).to_contain_text(
        f"Copy lessonEdit lessonDelete lesson{data['subject_name']}{new_lesson_type}{data['teacher_short']}{data['hour_value']} hour"
    )

def delete_lesson(page: Page, group_name: str):
    page.get_by_role("img", name="Delete lesson").click()
    page.get_by_role("button", name="Yes").click()

    expect(page.locator("#root")).to_contain_text(f"There are no lessons for group {group_name}")


def test_lessons_ced(setup_page: Page):
    data = {
        "group_name": "101-А",
        "teacher_name": "Бігун Ярослав Йосипович (професор)",
        "teacher_short": "Бігун Я. Й.",
        "subject_name": "Фізичне виховання",
        "lesson_type": "Practical",
        "hour_value": "1"
    }

    new_lesson_type="Lecture"

    login(setup_page)
    check_lessons_page(setup_page)

    create_lesson(setup_page, data)
    edit_lesson(setup_page, data, new_lesson_type)
    delete_lesson(setup_page, data["group_name"])

