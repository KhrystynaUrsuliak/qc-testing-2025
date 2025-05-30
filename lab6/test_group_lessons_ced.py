import re
from playwright.sync_api import Playwright, sync_playwright, expect, Page

from test_lessons_access import login, check_lessons_page

def create_grouped_lesson(page: Page, data: dict):
    page.get_by_role("combobox").filter(has_text="Group").locator('[aria-label="Open"]').click()
    page.get_by_role("option", name=data["group_name"]).click()

    page.get_by_role("combobox").filter(has_text="Teacher").locator('[aria-label="Open"]').click()
    page.get_by_role("option", name=data["teacher_name"]).click()
    page.get_by_role("textbox", name="Subject", exact=True).click()
    page.get_by_role("option", name=data["subject_name"]).click()
    page.get_by_role("combobox").filter(has_text="Type").locator('[aria-label="Open"]').click()
    page.get_by_role("option", name=data["lesson_type"]).click()
    page.get_by_role("textbox", name="Hour").click()
    page.get_by_role("textbox", name="Hour").fill(data["hour_value"])
    page.get_by_role("combobox").filter(has_text="Group").locator('[aria-label="Open"]').click()
    page.get_by_role("option", name=data["group_name"]).click()

    page.get_by_role("checkbox", name="Grouped").check()
    page.get_by_role("button", name="Copy for...").click()
    page.locator("#search_input").click()

    for group in data["additional_groups"]:
        page.get_by_text(group, exact=True).click()

    page.get_by_role("button", name="Copy for...").click()
    page.get_by_role("button", name="Save").click()


def check_all_groups_for_grouped_lesson(page: Page, data: dict):

    groups_to_check = [data["group_name"]] + data["additional_groups"]
    expected_text = (f"GroupedCopy lessonEdit lessonDelete lesson"f"{data['subject_name']}{data['lesson_type']}{data['teacher_short']}{data['hour_value']} hour")

    for group in groups_to_check:
        page.get_by_role("combobox").filter(has_text="Group").locator('[aria-label="Open"]').click()
        page.get_by_role("option", name=group).click()
        expect(page.locator("#root")).to_contain_text(expected_text)


def edit_grouped_lesson(page: Page, data: dict, new_lesson_type: str):

    page.get_by_role("combobox").filter(has_text="Group").locator('[aria-label="Open"]').click()
    page.get_by_role("option", name=data["group_name"]).click()

    page.get_by_role("img", name="Edit lesson").locator("path").click()

    page.get_by_role("combobox").filter(has_text="Type").locator('[aria-label="Open"]').click()
    page.get_by_role("option", name=new_lesson_type).click()

    page.get_by_role("button", name="Save").click()
    data["lesson_type"] = new_lesson_type


def delete_grouped_lesson(page: Page, data: dict):

    page.get_by_role("combobox").filter(has_text="Group").locator('[aria-label="Open"]').click()
    page.get_by_role("option", name=data["group_name"]).click()

    page.get_by_role("img", name="Delete lesson").click()
    page.get_by_role("button", name="Yes").click()

    page.get_by_role("combobox").filter(has_text="Group").locator('[aria-label="Open"]').click()
    page.get_by_role("option", name=data["group_name"]).click()
    expect(page.locator("#root")).to_contain_text(f"There are no lessons for group {data['group_name']}")

    for group in data["additional_groups"]:
        page.get_by_role("combobox").filter(has_text="Group").locator('[aria-label="Open"]').click()
        page.get_by_role("option", name=group).click()
        expect(page.locator("#root")).to_contain_text(f"There are no lessons for group {group}")


def test_grouped_lessons_ced(setup_page: Page):
    data = {
        "group_name": "102-А",
        "teacher_name": "Бігун Ярослав Йосипович (професор)",
        "teacher_short": "Бігун Я. Й.",
        "subject_name": "Фізичне виховання",
        "lesson_type": "Practical",
        "hour_value": "1",
        "additional_groups": ["101-Б", "107"]
    }

    new_lesson_type = "Lecture"

    login(setup_page)
    check_lessons_page(setup_page)

    create_grouped_lesson(setup_page, data)
    check_all_groups_for_grouped_lesson(setup_page, data)

    edit_grouped_lesson(setup_page, data, new_lesson_type)
    check_all_groups_for_grouped_lesson(setup_page, data)

    delete_grouped_lesson(setup_page, data)
