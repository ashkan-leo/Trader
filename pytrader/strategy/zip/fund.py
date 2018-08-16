import pandas as pd
from zipline.finance.execution import StopOrder
from zipline.utils.events import date_rules, time_rules

from pytrader.strategy.zip.Strategy import Strategy
from zipline.api import *
import pickle
from pytrader.fundamentals.dao import get_fundamentals, query
from pytrader.fundamentals.model import fundamentals


class Fund(Strategy):
    def initialize(self, context):
        context.limit = 10

        rebalance = lambda x, y: self.rebalance(x, y)
        schedule_function(rebalance,
                          date_rule=date_rules.every_day(),
                          time_rule=time_rules.market_open())
        pass

    def rebalance(self, context, data):
        for stock in context.portfolio.positions:
            if stock not in context.fundemantals and stock in data:
                order_target_percent(stock, 0)

    def before_trading_start(self, context, data):
        context.fundamentals = get_fundamentals(
            query(
                fundamentals.valuation_ratios.pb_ratio,
                fundamentals.valuation_ratios.pe_ratio
            ).filter(
                fundamentals.valuation_ratios.pe_ratio < 14
            ).filter(
                fundamentals.valuation_ratios.pb_ratio < 2
            ).orderby(
                fundamentals.valuation.market_cap.desc()
            ).limit(context.limit))

    def handle_data(self, context, data):
        cash = context.portfolio.cash
        current_positions = context.portfolio.positions

        for stock in data:
            current_position = current_positions[stock].amount
            stock_price = data[stock].price
            plausible_investment = cash / 10.0
            stop_price = stock_price - (stock_price * .005)

            share_amount = int(plausible_investment / stock_price)

            if stock_price < plausible_investment and current_position == 0:
                if context.fundamentals[stock]['pe_ratio'] < 11:
                    order(stock, share_amount, style=StopOrder(stop_price))


start = pd.to_datetime('2014-06-17').tz_localize('US/Eastern')
end = pd.to_datetime('2015-06-17').tz_localize('US/Eastern')

perf = Fund().run(start, end)
pickle.dump(perf, open("../portfolio/Fund.py..2014-06-17.2015-06-17.pickle", 'wb'))
