from selenium import webdriver
import os
from bs4 import BeautifulSoup
from scrappers.constants_scrappers import Constants, FileNames
import time
import logging
import json
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)


def load_browser():
    ############# GET WEB DRIVERS PATH #############
    directory_path = os.path.dirname(os.path.realpath(__file__))
    path_webdrivers = directory_path + "/" + FileNames.WEBDRIVER_UBUNTU

    ############# LOAD BROWSER #############
    browser_options = webdriver.ChromeOptions()
    browser = webdriver.Chrome(path_webdrivers, chrome_options=browser_options)
    return browser


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


def launch_scrapper():
    ############# OPEN BROWSER #############
    browser = load_browser()
    while True:  # Don't close the browser
        json_response = scrap_web(browser)
        # -----------> KAFKA connected with the json_response
        time.sleep(Constants.FREQUENCY_SCRAPPING_MS / 1000)
    # browser.quit()


if __name__ == "__main__":
    launch_scrapper()

