"""
A simple algo to run the 9 day RSI.  Much of this code came from Dan Whitable's (https://www.quantopian.com/users/571d1bab2616ef09ce0002b6) algorithim from this, https://www.quantopian.com/posts/trading-on-the-rsi-of-the-vix-and-spy, forum discussion.

The purpose of this script is to backtest a simple buy/sell strategy using the RSI 9 day.  The buy signal is a RSI < 30 and the sell signal is a RSI 9 > 70.
"""

import numpy as np

from quantopian.algorithm import attach_pipeline, pipeline_output
from quantopian.pipeline import Pipeline, CustomFilter
from quantopian.pipeline.data.builtin import USEquityPricing
from quantopian.pipeline.factors import RSI, Latest

from quantopian.pipeline.data import morningstar
 
def initialize(context):
    """
    Called once at the start of the algorithm.
    """
    #Generic name for equity traded, simply change the ticker
    #symbol to get any stock.
    context.stock_traded = symbol('ZUMZ')
    #To set the benchmark simply change the ticker symbol and
    #simply comment this line out for the SPX benchmark.
    set_benchmark(symbol('ZUMZ'))
    
    context.invested = False
    context.leverage = 1.0
    context.short = False
    # Rebalance every day, 1 hour after market open.
    schedule_function(my_rebalance, date_rules.every_day(), time_rules.market_open(hours=1))
     
    # Record tracking variables at the end of each day.
    schedule_function(my_record_vars, date_rules.every_day(), time_rules.market_close())
    
    schedule_function(trade, date_rules.every_day(), time_rules.market_open())

     
    # Create our dynamic stock selector.
    attach_pipeline(make_pipeline(context), 'my_pipeline')
         
def make_pipeline(context):
    """
    A function to create our dynamic stock selector (pipeline). Documentation on
    pipeline can be found here: https://www.quantopian.com/help#pipeline-title
    """
    
    rsi_filter = SidInList(sid_list = context.stock_traded.sid)
    
    close = Latest(
        inputs = [USEquityPricing.close],
        mask = rsi_filter,
    )
    
    rsi_9 = RSI(
        inputs = [USEquityPricing.close],
        window_length = 9,
        mask = rsi_filter,
    )
     
    pipe = Pipeline()
    
    pipe.add(close, 'close')
    pipe.add(rsi_9, 'rsi_9')
    
    pipe.set_screen(rsi_filter)
    
    return pipe
 
def before_trading_start(context, data):
    """
    Called every day before market open.
    """
    context.output = pipeline_output('my_pipeline')
  
    # These are the securities that we are interested in trading each day.
    context.security_list = context.output.index
     
def trade (context, data):    

    results = pipeline_output('my_pipeline')
                        
    stck = context.stock_traded   
    stck_close = results.loc[stck].close
    stck_rsi = results.loc[stck].rsi_9                    
                        
    if not context.invested:
        if stck_rsi < 30:
            order_target_percent(stck, context.leverage)
            context.invested = True
            context.short = False
    else:
        if stck_rsi > 70:
            order_target(stck, 0)
            context.invested = False
        
    
    # Record decisions made by algo:
    if context.invested:
        if context.short:
            position = -100.0
        else:
            position = 100.0
    else:
        position = 0.0
    
    record(stck_rsi = stck_rsi,
           stck = stck_close,
           pos = position,
          )


class SidInList(CustomFilter):
    """
    Filter returns True for any SID included in parameter tuple passed at creation.
    Usage: my_filter = SidInList(sid_list=(23911, 46631))
    """    
    inputs = []
    window_length = 1
    params = ('sid_list',)

    def compute(self, today, assets, out, sid_list):
        out[:] = np.in1d(assets, sid_list)  