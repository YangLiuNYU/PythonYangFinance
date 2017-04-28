#!/usr/bin/python

import sys
from Stock import Stock
from NasdaqTracker import NasdaqTracker
from YahooFinanceTracker import YahooFinanceTracker

def is_good_stock(stock):
    return (stock.m_earnings_per_share != None
            and stock.m_price_earnings_ratio != None
            and float(stock.m_price_earnings_ratio) <= 20
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

    yahoo_tracker = YahooFinanceTracker()
    yahoo_stocks = yahoo_tracker.get_data_from_yahoo(symbols)
    
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
