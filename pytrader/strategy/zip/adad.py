import numpy as np
import pandas as pd
from zipline._protocol import BarData

from pytrader.strategy.Strategy import Strategy
from pytrader.strategy.dma import DMA
from zipline.api import *
import datetime
import pickle
import random

class AdaD(Strategy):

    def __init__(self, asset, short, long, epsilon, frequency='1d'):
        self.short = short
        self.long = long
        self.epsilon = epsilon
        self.max_days = 100
        self.frequency = frequency

        super().__init__(asset)

    def initialize(self, context):
        context.asset = symbol(self.assets[0])
        context.short = self.short
        context.long = self.long
        context.epsilon = self.epsilon
        context.max_days = self.max_days

    def eval_strategy(self, start_date, end_date, short, long):
        dma_strategy = DMA(self.assets, short, long, self.frequency)
        perf = dma_strategy.run(start_date, end_date)
        returns = perf['returns']
        sharpe_ratio = np.sqrt(252) * (returns.mean() / (returns.std() + 0.0001))
        return sharpe_ratio

    def handle_data(self, context, data):
        short_mavg = data.history(context.asset, 'price', bar_count=context.short, frequency=self.frequency).mean()
        long_mavg = data.history(context.asset, 'price', bar_count=context.long, frequency=self.frequency).mean()

        # Trading logic
        if short_mavg > long_mavg:
            # order_target orders as many shares as needed to
            # achieve the desired number of shares.
            order_target(context.asset, 100)
        elif short_mavg < long_mavg:
            order_target(context.asset, 0)

        # Save values for later inspection
        record(price=data.current(context.asset, 'price'),
               short_mavg=short_mavg,
               long_mavg=long_mavg)
        pass

    def before_trading_start(self, context, data: BarData):
        today = data.current_dt
        n_days_ago = today - datetime.timedelta(days=context.max_days)

        p = self.eval_strategy(n_days_ago, today, context.short, context.long)
        px = self.eval_strategy(n_days_ago, today, context.short + context.epsilon, context.long)
        py = self.eval_strategy(n_days_ago, today, context.short, context.long + context.epsilon)

        delta_x = int(round(- p + px))
        delta_y = int(round(- p + py))
        print("starting day %s" % str(today))
        context.short = max(context.short + delta_x, 1)
        context.long = max(context.long + delta_y, 2)

        print(context.long, context.short)


start = pd.to_datetime('2015-01-01').tz_localize('US/Eastern')
end = pd.to_datetime('2015-12-31').tz_localize('US/Eastern')

perf = AdaD(["AAPL"], 5, 20, 2).run(start, end)
pickle.dump(perf, open("../portfolio/adad.py.AAPL.2015-01-01.2015-12-31.pickle", 'wb'))
