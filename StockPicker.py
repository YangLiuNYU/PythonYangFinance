#!/usr/bin/python

import csv
import sys
import requests
import json
import StringIO
from yahoo_finance import Share

class Stock:
    def __init__(self):
        self.m_symbol = None
        self.m_company = None
        self.m_price = None
        self.m_industry = None
        self.m_price_earnings_ratio = None
        self.m_earnings_per_share = None
        self.m_peg_ratio = None
        self.m_dividend_yield = None
        
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
        


class YahooFinanceTracker:
    """
    A class to pull information from Yahoo Finance
    """
    def __init__(self):
        self.yahoo_url = "http://finance.yahoo.com/d/quotes.csv?"

    def add_symbols(self, symbols):
        self.yahoo_url += "s=" + symbols
        return self

    def add_fields(self, fields):
        self.yahoo_url += "&f=" + fields
        return self

    def get_data(self):
        #print self.yahoo_url
        resp = requests.get(self.yahoo_url)
        text = resp.iter_lines()
        reader = csv.reader(text, delimiter=',')
        data = []
        for row in reader:
            data.append(row)
        return data
    

def get_data_from_yahoo(symbols_list):
    """
    Send request to Yahoo API in bulk.
    s : symbol
    e: Earnings per Share
    r: P/E Ratio
    r2: P/E Ratio (Realtime)
    r5: PEG Ratio
    y: Dividend Yield
    """
    bulk_symbols = []
    index = 0
    symbols_amount = len(symbols_list)
    stocks = {}
    for symbol in symbols_list:
        ++ index
        bulk_symbols.append(symbol)
        if len(bulk_symbols) == 100 or index == symbols_amount:
            symbols = ",".join(x for x in bulk_symbols)
            yahoo_finance_tracker = YahooFinanceTracker()
            data = yahoo_finance_tracker.add_symbols(symbols).add_fields("s,e,r,r5,y").get_data()
            for row in  data:
                stock = Stock()
                stock.m_symbol = row[0]
                if row[2].upper() != "N/A" :
                    stock.m_earnings_per_share = row[2]
                if row[4].upper() != "N/A" :
                    stock.m_price_earnings_ratio = row[4]
                if row[6].upper() != "N/A" :
                    stock.m_peg_ratio = row[6]
                if row[8].upper() != "N/A" :
                    stock.m_dividend_yield = row[8]
                stocks[stock.m_symbol] = stock
                #print stock.to_json()
            bulk_symbols = [] # clear bulk
    return stocks


def is_good_stock(stock):
    return (stock.m_earnings_per_share != None
            and stock.m_price_earnings_ratio != None
            and float(stock.m_price_earnings_ratio) <= 15
            and stock.m_dividend_yield != None
            and float(stock.m_dividend_yield) >= 1
            and stock.m_peg_ratio != None
            and float(stock.m_peg_ratio) < 5 and float(stock.m_peg_ratio) > 0)
    

if __name__ == "__main__":
    #print get_pe_ratio("GOOG")
    nasdaq_tracker = NasdaqTracker()
    nasdaq_stocks = nasdaq_tracker.pull_data()
    print "Total stocks : " + str(len(nasdaq_stocks))

    symbols = []
    for key in nasdaq_stocks:
        symbols.append(key)
    
    yahoo_stocks = get_data_from_yahoo(symbols)
    
    for symbol in yahoo_stocks:
        if symbol in nasdaq_stocks:
            nasdaq_stocks[symbol].m_earnings_per_share = yahoo_stocks[symbol].m_earnings_per_share
            nasdaq_stocks[symbol].m_price_earnings_ratio = yahoo_stocks[symbol].m_price_earnings_ratio
            nasdaq_stocks[symbol].m_peg_ratio = yahoo_stocks[symbol].m_peg_ratio
            nasdaq_stocks[symbol].m_dividend_yield = yahoo_stocks[symbol].m_dividend_yield

    good_stocks = []
    for stock in nasdaq_stocks:
        if is_good_stock( nasdaq_stocks[stock] ) :
            good_stocks.append(nasdaq_stocks[stock])

    # Sorting
    good_stocks.sort(key=lambda x: x.m_peg_ratio, reverse=True)
    
    for stock in good_stocks:
        print stock.to_json()

        
    print "Good stocks : " + str(len(good_stocks))
    sys.exit(0)
