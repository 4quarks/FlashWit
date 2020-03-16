from selenium import webdriver
import os
from bs4 import BeautifulSoup
from enum import Enum


class PropertiesAction:
    def __init__(self):
        self.labels = []
        self.settings = []
        self.correct_len = len(self.labels) == len(self.settings)


class FINDBY(Enum):
    FIND_BY_ID = 1
    FIND_BY_CLASS = 2
    FIND_BY_XPATH = 3


class TODO(Enum):
    SEND_KEYS = 4
    EXECUTE_WRITE = 5
    EXECUTE_CLICK = 6
    SIMPLE_CLICK = 7
    ACTION_CHAIN = 8


class Label:
    def __init__(self, header='', group='', reference='', xpath=''):
        self.header = header
        self.group = group
        self.reference = reference
        self.xpath = xpath
        self.find_all = False
        self.select = False
        self.typeAction()

    def typeAction(self):
        if self.reference:
            if self.header and self.group:
                self.find_all = True
            else:
                self.select = True


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


def get_scrap_data(place_to_search, labels, get_selenium=False):
    list_data = []
    scraped_data = None
    for label in labels:
        if label.find_all:
            scraped_data = place_to_search.findAll(label.header, {label.group: label.reference})
        elif label.select:
            scraped_data = place_to_search.select(label.reference)
        if scraped_data:
            if not get_selenium:
                [list_data.append(element_found.get_text()) for element_found in scraped_data]
            else:
                list_data.append(scraped_data)
    return list_data


if __name__ == "__main__":
    website = "https://tradingeconomics.com/stocks"
    response = load_web_scraper(website)
    soup = BeautifulSoup(response, 'html.parser')
    propierties_data = PropertiesAction()
    scraped_data = soup.findAll('tr', {'class': ['datatable-row', "datatable-row-alternating"]})
    for row in scraped_data:
        print(row.findAll('td', {'id': 'p'}))
    print(scraped_data)
