from zipline.api import *
import os
from abc import ABC, abstractmethod
from datetime import datetime
from zipline import run_algorithm
import pytz


class Strategy(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def initialize(self, context):
        pass

    @abstractmethod
    def handle_data(self, context, data):
        pass

    def before_trading_start(self, context, data):
        pass

    def run(self, start_date, end_date, capital_base=10000, bundle='quantopian-quandl'):
        initialize = lambda context: self.initialize(context)
        handle_data = lambda context, data: self.handle_data(context, data)
        before_trading_start = lambda context, data: self.before_trading_start(context, data)

        perf = run_algorithm(start_date, end_date,
                             initialize,
                             capital_base,
                             handle_data,
                             before_trading_start,
                             bundle=bundle)
        return perf
