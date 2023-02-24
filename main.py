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

import data_handler

options = Options()
options.add_experimental_option("detach", False)  # if True - keep browser open after script is done (for debugging)

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),
                          options=options,
                          )

def parse_prices(item):
    """
    Parse prices from an item
    :return: dict with city-price pairs
    """
    item_prices = {}
    item_price = "0"

    item_spans = item.find_elements("xpath", ".//span")
    for span in item_spans:
        item_city_name = span.get_attribute("title")
        item_price = span.text.replace(",", "")
        if item_price != "":
            item_prices[item_city_name] = int(item_price)

    # make dataframe row with index and correct price positions
    formatted_city_price = data_handler.city_formatter(item_prices)

    return formatted_city_price


def parse_items(item_data, subcat_url):
    """
    :param item_data: dataframe with items
    :param subcat_url: url to parse
    Parse items from subcat_url
    Each item has name, enchantment lvl (0-3), unique id, and dict with city-price pairs
    :return item_data: dataframe with old and new data
    """
    driver.get(subcat_url)
    items = driver.find_elements("xpath", "//div[@class='row'][4]//a")
    time.sleep(3)
    for item in items:
        item_temp_data = []
        item_title = item.text.split("\n")[0]

        # check if item has enchantment lvl
        enchantment_lvl = 0
        item_href_last_symbol = item.get_attribute("href")[-2:]

        if item_href_last_symbol in ("@1", "@2", "@3"):
            enchantment_lvl = int(item_href_last_symbol[-1])

        item_prices = parse_prices(item)
        item_temp_data = (item_title, enchantment_lvl, item_prices)
        item_calc_data = data_handler.item_data_formatter(item_temp_data)

        # add formatted and calculated data to total dataframe
        for item_calc in item_calc_data:
            item_data = data_handler.df_append(item_data, item_calc)

    return item_data


def main():
    """
    Loop through all subcategories
    """
    start_time = time.time()
    item_data = data_handler.create_dataframe()

    with open("subcats.json", "r") as read_file:
        subcat_urls = json.load(read_file)

    # for testing purposes if you need to change something and don't want to parse all subcats
    # subcat_urls = ["https://albiononline2d.com/en/item/cat/armor/subcat/cloth_armor"]


    subcat_counter = 0
    for subcat_url in subcat_urls:

        print(f'Parsing cat #{subcat_counter} by url: {subcat_url}')
        item_data = parse_items(item_data, subcat_url)
        print("Total time: --- %s seconds ---" % (time.time() - start_time))

        subcat_counter += 1

    print(item_data)
    # upload data to google sheets
    data_handler.sheet_updater(item_data)

    print("--> Total subcategories: ", subcat_counter)
    # time for script to run
    print("--- %s minutes ---" % ((time.time() - start_time)/60))

if __name__ == "__main__":
    main()