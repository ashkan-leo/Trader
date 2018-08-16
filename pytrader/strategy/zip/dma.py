from zipline.api import *

from pytrader.strategy.zip.Strategy import Strategy


class DMA(Strategy):

    def __init__(self, assets: [], short=32, long=256, frequency="1d"):
        super().__init__(assets)
        self.short = short
        self.long = long
        self.frequency = frequency

    def initialize(self, context):
        context.i = 0
        context.asset = symbol(self.assets[0])
        context.short = self.short
        context.long = self.long

    def handle_data(self, context, data):
        # Skip first 300 days to get full windows
        context.i += 1
        if context.i < context.long:
            return

        # Compute averages
        # data.history() has to be called with the same params
        # from above and returns a pandas dataframe.

        # With probability p, pick a value between up and down.
        # With probability 1 - p pick a value less t

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

    def run(self, start_date, end_date, capital_base=10000, bundle='quantopian-quandl'):
        perf = super().run(start_date, end_date, capital_base, bundle)
        return perf
