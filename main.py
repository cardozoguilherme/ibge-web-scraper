from playwright.sync_api import sync_playwright, Playwright
import re, csv
from xpaths import (
    POPULATION_XPATHS,
    EDUCATION_XPATHS,
    WORK_AND_INCOME_XPATHS,
    ECONOMY_XPATHS,
    TERRITORY_XPATHS,
)

SECTIONS = {
    "population": POPULATION_XPATHS,
    "education": EDUCATION_XPATHS,
    "work_and_income": WORK_AND_INCOME_XPATHS,
    "economy": ECONOMY_XPATHS,
    "territory": TERRITORY_XPATHS,
}


def extract_section_data(page, xpath_map):
    data = {}
    for label_xpath, value_xpath in xpath_map.items():
        label = re.sub(
            r"\s+", " ", page.locator(f"xpath={label_xpath}").text_content().strip()
        )
        value = page.locator(f"xpath={value_xpath}").text_content().strip()
        data[label] = value
    return data


def save_csv(filename, data):
    fieldnames = ["Estado"] + [key for key in data[0] if key != "Estado"]
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)


def run(playwright: Playwright):
    browser = playwright.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://cidades.ibge.gov.br/")

    page.locator("#abaMenuLateral").click()
    page.locator("#menu__estado").click()
    page.wait_for_load_state

    links = page.locator("a[href^='/brasil/']")
    states = []

    for i in range(links.count()):
        href = links.nth(i).get_attribute("href")
        if re.fullmatch(r"/brasil/[a-z]{2}", href):
            name = links.nth(i).text_content().strip()
            states.append({"name": name, "link": href})

    section_data = {name: [] for name in SECTIONS}

    for state in states:
        print(f"\nExtracting data from {state['name']}...")
        page.goto("https://cidades.ibge.gov.br" + state["link"])
        page.wait_for_load_state

        for section, xpaths in SECTIONS.items():
            data = extract_section_data(page, xpaths)
            data["Estado"] = state["name"]
            section_data[section].append(data)

    browser.close()

    for section, data in section_data.items():
        save_csv(f"extracted_data/{section}.csv", data)


with sync_playwright() as playwright:
    run(playwright)
