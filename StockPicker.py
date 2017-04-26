#!/usr/bin/python

import csv
import sys
import requests
import json
from yahoo_finance import Share

class Stock:
    def __init__(self):
        self.m_symbol = None
        self.m_company = None
        self.m_price = None
        self.m_industry = None
        self.m_price_earnings_ratio = None
        
    def to_json(self):
        """
        Serilization.
        """
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)

class NasdaqTracker:
    """
    A class to pull tickers list from Nasdap.
    """
    def __init__(self):
        self.nasdaq_url = "http://www.nasdaq.com/screening/companies-by-name.aspx?letter=0&exchange=nasdaq&render=download"
        
    def pull_data(self):
        resp = requests.get(self.nasdaq_url)
        text = resp.iter_lines()
        reader = csv.reader(text, delimiter=',')
        next(reader, None)  # skip the headers
        stock_lists = []
        for row in reader:
            stock = Stock()
            if len(row) > 3 :
                stock.m_symbol = row[0]
                stock.m_company = row[1]
                stock.m_price = row[2]
                stock.m_industry = row[5]
                stock_lists.append(stock)
                
        return stock_lists
        



def get_data_from_yahoo(stock_list):
    for stock in stock_list:
        share = Share(stock.m_symbol)
        stock.m_price_earnings_ratio = share.get_price_earnings_ratio()
    return stock_list


if __name__ == "__main__":
    #print get_pe_ratio("GOOG")
    nasdaq_tracker = NasdaqTracker()
    stock_list = nasdaq_tracker.pull_data()
    print "Total stocks : " + str(len(stock_list))
    stock_list = stock_list[:100]
    stock_list = get_data_from_yahoo(stock_list)
    for stock in stock_list:
        print stock.to_json()
    sys.exit(0)
