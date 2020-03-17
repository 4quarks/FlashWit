from selenium import webdriver
import os
from bs4 import BeautifulSoup
from scrappers.constants_scrappers import Constants
import time

def load_web_driver():
    path_webdrivers = os.path.dirname(os.path.realpath(__file__)) + "/"
    os.environ["PATH"] += ";" + path_webdrivers
    print('AAA' + path_webdrivers)
    browser_options = webdriver.ChromeOptions()
    browser = webdriver.Chrome(path_webdrivers + "chromedriver", chrome_options=browser_options)

    return browser


def load_web_scraper(site):
    browser = load_web_driver()
    browser.refresh()
    browser.get(site)
    browser.execute_script("window.scrollTo(0, 0)")
    return browser.page_source


if __name__ == "__main__":
    dict_result_scrapping = {}
    response = load_web_scraper(Constants.WEBSITE)
    soup = BeautifulSoup(response, 'html.parser')
    # scraped_data = soup.findAll('tr', {'class': ['datatable-row', "datatable-row-alternating"]})
    tables = soup.findAll('div', {'class': "table-responsive"})
    for country_market_bs4 in tables:
        row_head = country_market_bs4.findAll('thead')
        # headers = row_head[0].get_text().strip().split('\n')
        # clean_headers = [element.strip() for element in headers if element.strip() != '']
        country = row_head[0].findAll('th', {'style': "text-align: left;cursor: pointer;"})
        country_name = country[0].get_text().strip()
        dict_result_scrapping[country_name] = {}
        print('Country: ' + country_name)
        markets = country_market_bs4.findAll('tr', {'class': ['datatable-row', "datatable-row-alternating"]})
        for row_market_bs4 in markets:
            market_name_bs4 = row_market_bs4.findAll('td', {'class': 'datatable-item-first'})
            market_name = market_name_bs4[0].get_text().strip()
            print('Market name: ' + market_name)
            dict_result_scrapping[country_name][market_name] = {}
            value_market = row_market_bs4.findAll('td', {'class': 'datatable-item'})
            for index, value in enumerate(value_market):
                clean_value = value.get_text().strip()
                dict_result_scrapping[country_name][market_name][Constants.TAGS[index]] = clean_value
                print(Constants.TAGS[index] + ': ' + clean_value)
            print('*'*10)
    print()

