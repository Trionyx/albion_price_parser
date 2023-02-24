# methods to work with the Google Spreadsheet
# tutorial: https://youtube.com/watch?v=aruInGd-m40

import json

import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd


from config import your_email

# Connect to Google
# Scope: Enable access to specific links
scope = ['https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive"]

credentials = ServiceAccountCredentials.from_json_keyfile_name("gs_credentials.json", scope)
client = gspread.authorize(credentials)

# Create a blank spreadsheet (Note: We're using a service account, so this spreadsheet is visible only to this account)
# sheet = client.create("albion-market-prices-hunter")

# To access newly created spreadsheet from Google Sheets with your own Google account you must share it with your email
# Sharing a Spreadsheet
# sheet.share(your_email, perm_type='user', role='writer')  # your_email from config.py

# initial dataframe
def create_dataframe():
    df = pd.DataFrame(columns=[
        'Item',
        'Ench lvl',
        'Caerleon price',
        'BlackMarket price',
        'From city',
        'From city price',
        'Spread Caerleon',
        'Spread BlackMarket',
    ])
    return df

# upload data to the spreadsheet
def sheet_updater(albion_data):
    # Open the spreadsheet
    sheet = client.open("albion-market-prices-hunter").sheet1
    # read incomming data with pandas
    # df = pd.DataFrame(albion_data)
    # sort data by spread Caerleon
    albion_data.sort_values(by=["Spread Caerleon"], inplace=True, ascending=False)
    # export df to a sheet
    sheet.update([albion_data.columns.values.tolist()] + albion_data.values.tolist())

def city_formatter(item_prices):
    """
    Format city names by model
    :param item_price: dict with city-price pairs
    :return: dict with formatted city-price pairs
    """
    formatted_city_price = {}

    # TMP for testing
    # with open('item_prices.json') as f:
    #     item_prices = json.load(f)

    if 'Caerleon' in item_prices:
        formatted_city_price['Caerleon'] = item_prices['Caerleon']
    else:
        formatted_city_price['Caerleon'] = None
    if 'Black Market' in item_prices:
        formatted_city_price['Black Market'] = item_prices['Black Market']
    else:
        formatted_city_price['Black Market'] = None
    if 'Bridgewatch' in item_prices:
        formatted_city_price['Bridgewatch'] = item_prices['Bridgewatch']
    else:
        formatted_city_price['Bridgewatch'] = None
    if 'Fort Sterling' in item_prices:
        formatted_city_price['Fort Sterling'] = item_prices['Fort Sterling']
    else:
        formatted_city_price['Fort Sterling'] = None
    if 'Lymhurst' in item_prices:
        formatted_city_price['Lymhurst'] = item_prices['Lymhurst']
    else:
        formatted_city_price['Lymhurst'] = None
    if 'Thetford' in item_prices:
        formatted_city_price['Thetford'] = item_prices['Thetford']
    else:
        formatted_city_price['Thetford'] = None
    if 'Martlock' in item_prices:
        formatted_city_price['Martlock'] = item_prices['Martlock']
    else:
        formatted_city_price['Martlock'] = None

    # print(formatted_city_price)
    return formatted_city_price



# make dataframe row with index and correct price positions
def format_prices(item_title, item_prices):
    """
    dataframe row with index and correct price positions
    :param item_title: item name
    :param item_prices: list with sorted prices by model
    :return: list with formatted prices
    """
    formatted_prices = []
    formatted_prices.append(item_title)
    for city, price in item_prices.items():
        formatted_prices.append(price)
    return formatted_prices

# save data to csv
def csv_saver(albion_data):
    df = pd.DataFrame(albion_data)
    df.to_csv("albion_data.csv")


def item_data_formatter(item_data):
    """
    Format item data by model
    :param item_data:
    :return: formatted item data
    """
    formatted_item_data = []

    # TODO filter critical values, like if spread more that 200% of item price
    for city in item_data[2]:
        if item_data[2].get(city) is not None:
            try:
                formatted_item_data.append([
                    item_data[0],
                    item_data[1],
                    item_data[2].get('Caerleon'),
                    item_data[2].get('Black Market'),
                    city,
                    item_data[2].get(city),
                    item_data[2].get('Caerleon')*0.92 - item_data[2].get(city),
                    item_data[2].get('Black Market')*0.92 - item_data[2].get(city),
                ])
            except TypeError:
                # print("TypeError: ", item_data[0], city, item_data[2].get(city))
                pass


    # print(formatted_item_data[2:])
    return formatted_item_data[2:]

def df_append(item_data, item_calc):
    """
    Append new data to the dataframe
    :param item_data: current dataframe
    :param item_calc: list with calculated data
    :return: None
    """

    new_row = pd.DataFrame({
        'Item': item_calc[0],
        'Ench lvl': item_calc[1],
        'Caerleon price': item_calc[2],
        'BlackMarket price': item_calc[3],
        'From city': item_calc[4],
        'From city price': item_calc[5],
        'Spread Caerleon': item_calc[6],
        'Spread BlackMarket': item_calc[7],},
        index=[0])

    item_data = pd.concat([new_row, item_data.loc[:]]).reset_index(drop=True)



    return item_data


# test data
# item_data_formatter((
#     "Adept's Cleric Robe",
#     1,
#     {
#          'Caerleon': 4679,
#          'Black Market': 9993,
#          'Bridgewatch': 6689,
#          'Fort Sterling': 4402,
#          'Lymhurst': None,
#          'Thetford': None,
#          'Martlock': None
#         }
# ))