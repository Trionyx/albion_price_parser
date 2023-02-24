# Parses categories and subcategories from https://albiononline2d.com/en/item
# and saves them to a json file
# Only use this if current cats.json and subcats.json don't work

import time
import json

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import InvalidArgumentException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager

import config

options = Options()
options.add_experimental_option("detach", True)  # Keep browser open after script is done (for debugging)

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),
                          options=options,
                          )
CAT_URL = "https://albiononline2d.com/en/item"


def parse_cat():
    driver.get(CAT_URL)
    time.sleep(1)

    categories = driver.find_elements("xpath", "//*[@id='itemsCategories']//a")

    categories_links = []
    for category in categories:
        categories_links.append(category.get_attribute("href"))

    return categories_links

def cats_to_json():
    with open('cats.json', 'w') as f:
        json.dump(parse_cat(), f)

def parse_subcats():
    with open('cats.json', 'r') as f:
        categories_links = json.load(f)

    subcategories_links = []
    for category in categories_links:
        driver.get(category)
        subcategories = driver.find_elements("xpath", "//*[@id='itemsCategories']//a")
        for subcategory in subcategories:
            # only add links that contain "/subcat/" in them
            if "/subcat/" in subcategory.get_attribute("href"):
                subcategories_links.append(subcategory.get_attribute("href"))

    return subcategories_links

def subcats_to_json():
    with open('subcats.json', 'w') as f:
        json.dump(parse_subcats(), f)
    pass


if __name__ == "__main__":
    cats_to_json()
    subcats_to_json()