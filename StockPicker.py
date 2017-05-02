#!/usr/bin/python

import sys
from Model.Stock import Stock
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

    # Combine the stock information from Yahoo and Nasdaq together
    for symbol in yahoo_stocks:
        if symbol in nasdaq_stocks:
            for attr, value in nasdaq_stocks[symbol].__dict__.iteritems():
                if hasattr(yahoo_stocks[symbol], attr) == False or getattr(yahoo_stocks[symbol], attr) is None:
                    if value is not None:
                        setattr(yahoo_stocks[symbol], attr, value)

    personal_strategy = PersonalStrategy()
    good_stocks = []
    for ticker in yahoo_stocks:
        if personal_strategy.stock_validation( yahoo_stocks[ticker] ) :
            good_stocks.append(yahoo_stocks[ticker])

    # Sorting
    good_stocks.sort(key=lambda x: x.m_peg_ratio, reverse=True)
    
    for stock in good_stocks:
        print stock.to_json()

        
    print "Good stocks : " + str(len(good_stocks))
    sys.exit(0)
