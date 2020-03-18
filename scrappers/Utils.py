from selenium import webdriver
import os
from bs4 import BeautifulSoup
from constants_scrappers import Constants, FileNames, PathFiles
import time
import logging
import json
import pandas as pd
from os import listdir
from os.path import isfile, join
import re

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)


def get_webdrivers_path():
    ############# GET WEB DRIVERS PATH #############
    directory_path = os.path.dirname(os.path.realpath(__file__))
    path_webdrivers = directory_path + "/" + PathFiles.WEBDRIVERS + '/' + FileNames.WEBDRIVER_UBUNTU
    return path_webdrivers, directory_path


def load_browser():
    path_webdrivers, directory_path = get_webdrivers_path()
    ############# LOAD BROWSER #############
    browser_options = webdriver.ChromeOptions()
    prefs = {"download.default_directory": directory_path + "/" + PathFiles.DOWNLOADS + "/",
             'helperApps.neverAsk.saveToDisk': 'text/csv'}  # Don't open window to download
    browser_options.add_experimental_option("prefs", prefs)
    browser_options.add_argument("--start-maximized")  # Full screen
    browser = webdriver.Chrome(path_webdrivers, chrome_options=browser_options)
    return browser


def quit_browser():
    path_webdrivers, directory_path = get_webdrivers_path()
    browser = webdriver.Chrome(path_webdrivers)
    browser.quit()


def get_web_html(browser, site):
    browser.get(site)
    page_source = browser.page_source
    web_html = BeautifulSoup(page_source, 'html.parser')
    return web_html


def refresh_browser(browser):
    browser.refresh()
    browser.execute_script("window.scrollTo(0, 0)")


def get_text_and_clean(bs4_list):
    return bs4_list[0].get_text().strip()


def scrap_web(browser):
    ############# GET WEBSITE'S HTML #############
    web_html = get_web_html(browser, Constants.WEBSITE)

    ############# FIND GENERAL TABLES OF CONTENT #############
    dict_result_scrapping = {}
    tables = web_html.findAll('div', {'class': "table-responsive"})

    ############# GET ROWS FROM EACH TABLE #############
    for country_market_bs4 in tables:
        row_head = country_market_bs4.findAll('thead')
        markets = country_market_bs4.findAll('tr', {'class': ['datatable-row', "datatable-row-alternating"]})

        # Get country from the first row (header row)
        country = row_head[0].findAll('th', {'style': "text-align: left;cursor: pointer;"})
        country_name = get_text_and_clean(country)

        # headers = row_head[0].get_text().strip().split('\n')
        # clean_headers = [element.strip() for element in headers if element.strip() != '']

        dict_result_scrapping[country_name] = {}
        logging.debug('Country: ' + country_name)

        ############# GET SPECIFIC VALUES FOR EACH MARKET #############
        for row_market_bs4 in markets:
            market_name_bs4 = row_market_bs4.findAll('td', {'class': 'datatable-item-first'})
            value_market = row_market_bs4.findAll('td', {'class': 'datatable-item'})

            # Get all the values from each row
            market_name = get_text_and_clean(market_name_bs4)

            dict_result_scrapping[country_name][market_name] = {}
            logging.debug('Market name: ' + market_name)

            ############# CLEAN VALUES #############
            for index, value in enumerate(value_market):
                clean_value = value.get_text().strip()
                dict_result_scrapping[country_name][market_name][Constants.TAGS[index]] = clean_value

                logging.debug(Constants.TAGS[index] + ': ' + clean_value)

            logging.debug('*' * 10)

    ############# JSON WITH ALL DATA COLLECTED #############
    json_result = json.dumps(dict_result_scrapping)
    return json_result


def download_files(list_companies, time_range):
    ############# OPEN BROWSER #############
    from selenium import webdriver
    browser = load_browser()
    # To prevent download dialog
    for company in list_companies:
        browser.get("https://www.nasdaq.com/market-activity/stocks/" + company + "/historical")

        banner = browser.find_elements_by_class_name("evidon-banner-icon")[0]
        time.sleep(1)
        banner.click()

        download_button = browser.find_elements_by_class_name('historical-data__download')[0]
        time.sleep(1)
        _ = download_button.location_once_scrolled_into_view

        max_data_category = browser.find_elements_by_xpath('//button[contains(text(), ' + time_range + ')]')[0]
        time.sleep(1)
        max_data_category.click()

        time.sleep(1)
        download_button.click()
        time.sleep(3)


def clean_data(list_companies):
    # Get the names of the files downloaded
    path_files = PathFiles.DOWNLOADS + '/'
    list_files = [f for f in listdir(path_files) if isfile(join(path_files, f))]

    for file in list_files:
        # THe number of the filename will give us the name of the company (download sorted)
        number_detected = re.findall(r'\d+', file)
        if not number_detected:
            number_file = 0
        else:
            number_file = int(number_detected[0])

        # Read downloaded data and clean it
        data = pd.read_csv(path_files + file)
        data.columns = Constants.COLUMNS_HISTORICAL_DATA
        for column in data.columns:
            data[column] = data[column].apply(lambda x: str(x).replace('$', ''))

        # Write new csv file
        data.to_csv(path_files + list_companies[number_file] + '.csv', index=False)


if __name__ == "__main__":
    load_browser()
    quit_browser()