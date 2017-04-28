#!/usr/bin/python
import requests
import csv
from Stock import Stock

class NasdaqTracker:
    """
    A class to pull tickers list from Nasdap.
    """
    def __init__(self):
        self.nasdaq_url = "http://www.nasdaq.com/screening/companies-by-name.aspx?letter=0&exchange=nasdaq&render=download"

        
    def pull_data(self):
        """
        Send http request to get stock information.
        Return a stocks HashMap, <"symbol", Stock>
        """
        resp = requests.get(self.nasdaq_url)
        text = resp.iter_lines()
        reader = csv.reader(text, delimiter=',')
        next(reader, None)  # skip the headers
        stocks = {}  # Stocks HashMap
        for row in reader:
            stock = Stock()
            if len(row) > 3 :
                stock.m_symbol = row[0]
                stock.m_company = row[1]
                stock.m_price = row[2]
                stock.m_industry = row[5]
                stocks[stock.m_symbol] = stock
        return stocks
