#!/usr/bin/python

from StockInvestmentStrategy import StockInvestmentStrategy

class PersonalStrategy(StockInvestmentStrategy):
    """
    My personal investment strategy
    """
        
    def stock_validation(self, stock):
        return (stock.m_earnings_per_share != None
                and stock.m_price_earnings_ratio != None
                and float(stock.m_price_earnings_ratio) <= 20
                and stock.m_dividend_yield != None
                and float(stock.m_dividend_yield) >= 1
                and stock.m_peg_ratio != None
                and float(stock.m_peg_ratio) < 5 and float(stock.m_peg_ratio) > 0)
