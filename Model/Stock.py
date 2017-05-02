#!/usr/bin/python
import json
class Stock:
    """
    Store stock related information.
    """
    def __init__(self):
        self.m_symbol = None
        self.m_company = None
        self.m_price = None
        self.m_industry = None
        self.m_price_earnings_ratio = None
        self.m_earnings_per_share = None
        self.m_peg_ratio = None
        self.m_dividend_yield = None
        self.m_market_cap = None
        self.m_cash_flow_per_share = None
        self.m_share_outstading = None
        self.m_trailing_twelve_months_sales = None
        
    def to_json(self):
        """
        Serilization.
        """
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)
