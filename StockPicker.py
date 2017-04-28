#!/usr/bin/python

import sys
from Stock import Stock
from DataCollector.NasdaqTracker import NasdaqTracker
from DataCollector.YahooFinanceTracker import YahooFinanceTracker
from InvestmentStrategy.PersonalStrategy import PersonalStrategy


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

    personal_strategy = PersonalStrategy()
    good_stocks = []
    for stock in nasdaq_stocks:
        if personal_strategy.stock_validation( nasdaq_stocks[stock] ) :
            good_stocks.append(nasdaq_stocks[stock])

    # Sorting
    good_stocks.sort(key=lambda x: x.m_peg_ratio, reverse=True)
    
    for stock in good_stocks:
        print stock.to_json()

        
    print "Good stocks : " + str(len(good_stocks))
    sys.exit(0)
