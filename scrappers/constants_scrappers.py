from enum import Enum


class Constants:
    TAGS = ['Price', 'Value', 'Daily', 'Weekly', 'Monthly', 'Yearly', 'Date']
    WEBSITE = "https://tradingeconomics.com/stocks"
    FREQUENCY_SCRAPPING_MS = 100
    COLUMNS_HISTORICAL_DATA = ["Date", "Close($)", "Volume", "Open($)", "High($)", "Low($)"]


class FileNames:
    WEBDRIVER_UBUNTU = "chromedriver"
    WEBDRIVER_MAC = "mac_chromedriver"


class PathFiles:
    DOWNLOADS = "downloads"
    WEBDRIVERS = "webdrivers"


class TimeRange(Enum):
    ONE_MONTH = '1M'
    SIX_MONTHS = '6M'
    ONE_YEAR = '1Y'
    FIVE_YEARS = '5Y'
    MAX = 'MAX'
    YTD = 'YTD'


