#!/usr/bin/python
import requests
import csv
from Model.Stock import Stock
from yahoo_finance import Share

class YahooFinanceUrlBuilder:
    """
    Build Yahoo Finance API url.
    """
    def __init__(self):
        self.yahoo_url = "http://finance.yahoo.com/d/quotes.csv?"

        
    def add_symbols(self, symbols):
        """
        Add comma-seprated symbols to url.
        """
        self.yahoo_url += "s=" + symbols
        return self

    
    def add_fields(self, fields):
        """
        Add comma-separated fields to url.
        """
        # API fields don't need seperator
        fields = fields.replace(',', '')
        self.yahoo_url += "&f=" + fields
        return self

    def get_url(self):
        """
        Return the constructed url.
        """
        return self.yahoo_url

    
class YahooFinanceTracker:
    """                                                                                                 
    A class to pull information from Yahoo Finance                                                        
    """
    def get_data(self, yahoo_url):
        """
        Return the information we get from Yahoo Finance API.
        """
        resp = requests.get(yahoo_url)
        text = resp.iter_lines()
        reader = csv.reader(text, delimiter=',')
        data = []
        for row in reader:
            data.append(row)
        return data


    def get_data_from_yahoo(self, symbols_list):
        """
        Return a Dictionary of <symbol, Stock>
        Send request to Yahoo API in bulk.
        s : symbol
        e: Earnings per Share
        r: P/E Ratio
        r2: P/E Ratio (Realtime)
        r5: PEG Ratio
        y: Dividend Yield
        j1 : market cap
        j2: Shares Outstanding
        
        """
        bulk_symbols = []
        index = 0
        symbols_amount = len(symbols_list)
        stocks = {}
        BULK_SIZE = 200
        
        for symbol in symbols_list:
            index += 1
            bulk_symbols.append(symbol)
            if len(bulk_symbols) == BULK_SIZE or index == symbols_amount:
                # Build the yahoo finance url with the bulk symbols
                symbols = ",".join(x for x in bulk_symbols)
                url_builder = YahooFinanceUrlBuilder()

                # Here add_fields method will get rid of these comma
                url_builder.add_symbols(symbols).add_fields("s,n,e,r,r5,y,j1")
                
                # Process data
                data = self.get_data(url_builder.get_url())
                for row in  data:
                    
                    stock = Stock()
                    stock.m_symbol = row[0]
                    stock.m_company = row[1]
                    stock.m_earnings_per_share = row[2]
                    stock.m_price_earnings_ratio = row[3]
                    stock.m_peg_ratio = row[4]
                    stock.m_dividend_yield = row[5]
                    stock.m_market_cap = row[6]

                    # Clear invalid values
                    for attr, value in stock.__dict__.iteritems():
                        if value == "N/A":
                            setattr(stock, attr, None)
                            
                        
                    stocks[stock.m_symbol] = stock
            
                bulk_symbols = [] # clear bulk
                
        
        return stocks



if __name__ == "__main__":
    tracker = YahooFinanceTracker()
    data = tracker.get_data_from_yahoo(["GOOG","FB","GILD","AAPL"])
    for symbol in data:
        print data[symbol].to_json()
    
