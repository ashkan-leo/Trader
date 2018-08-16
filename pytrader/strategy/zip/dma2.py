from zipline.api import *
import os

SYM = os.environ['SYM']


def initialize(context):
    context.i = 0
    context.asset = symbol(SYM)


def handle_data(context, data):
    # Skip first 300 days to get full windows
    context.i += 1
    if context.i < 300:
        return

    # Compute averages
    # data.history() has to be called with the same params
    # from above and returns a pandas dataframe.
    short_mavg = data.history(context.asset, 'price', bar_count=20, frequency="1d").mean()
    long_mavg = data.history(context.asset, 'price', bar_count=50, frequency="1d").mean()

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
