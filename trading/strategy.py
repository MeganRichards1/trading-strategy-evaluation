# Functions to implement our trading strategy.
import numpy as np
import trading.process as proc
import random as rand
import trading.indicators as indic


def random(stock_prices, period=7, amount=5000, fees=20, ledger='ledger_random.txt'):
    '''
    Randomly decide, every period, which stocks to purchase,
    do nothing, or sell (with equal probability).
    Spend a maximum of amount on every purchase.

    Input:
        stock_prices (ndarray): the stock price data
        period (int, default 7): how often we buy/sell (days)
        amount (float, default 5000): how much we spend on each purchase
            (must cover fees)
        fees (float, default 20): transaction fees
        ledger (str): path to the ledger file

    Output: None
    '''
    
    number_of_stocks = len(stock_prices[0])  # how many stocks we own
    time = len(stock_prices[:,0])            # how many days worth of data
    no_of_decisions = (time - 1) // period   # how many periods elapse excl final day where we sell
    
    available_amounts = amount / number_of_stocks  # split money evenly
   
    
    # create portfolio on day 0 with equally split shares
    portfolio = proc.create_portfolio(available_amounts, stock_prices, fees, ledger)
    
    for i in range(1, no_of_decisions):       # decide every period
        date = i * period                     # the day we make the decision on
        
        for j in range(number_of_stocks):     # decide which stocks to sell
            stock = j
            decision = rand.choice([1, 2, 3]) # choice of 3 options with equal weightings

            if decision == 1:                 #... option 1 is buy...
                proc.buy(date, stock, amount, stock_prices, fees, portfolio, ledger)

            elif decision == 2:               #... option 2 is sell...
                if portfolio[stock] == 0:     # can't sell if you have no stocks
                    pass
                else:
                    proc.sell(date, stock, stock_prices, fees, portfolio, ledger)   
            else:
                pass                          #... option 3 is do nothing.
    
    for stock_no in range(number_of_stocks):  # sell all stocks on final day
        # Note: portfolio can still contain some shares of failed companies at end of day
        date = (time - 1)
        stock = stock_no
        if portfolio[stock] == 0:     # if have no stocks to sell, pass
            pass
        else:
            proc.sell(date, stock, stock_prices, fees, portfolio, ledger)

    
    
def crossing_averages(stock_prices, n=200, m=50, weights=[], amount=5000, fees=20, ledger='ledger_crossing_points.txt'):
    '''
    Finds the crossing points between a SMA with period n and a FMA with period m
    and either buys or sells relevant stocks at these dates. Otherwise, does nothing. 
    Spend a maximum of amount on every purchase.

    Input:
        stock_prices (ndarray): the stock price data
        period (int, default 7): how often we buy/sell (days)
        amount (float, default 5000): how much we spend on each purchase
            (must cover fees)
        fees (float, default 20): transaction fees
        ledger (str): path to the ledger file

    Output: None
    '''
    
    number_of_stocks = len(stock_prices[0])  # how many stocks we own
    time = len(stock_prices[:,0])            # how many days worth of data
    
    available_amounts = amount / number_of_stocks  # split money evenly
    
    # create portfolio on day 0 with equally split shares
    portfolio = proc.create_portfolio(available_amounts, stock_prices, fees, ledger)
    
    for i in range(number_of_stocks): # get individual stock price over time for each stock
        stock_price = stock_prices[:, i]
        stock = i
        
        # get SMA and FMA of the stock
        SMA = indic.moving_average(stock_price, n, weights)
        FMA = indic.moving_average(stock_price, m, weights)
        
        for j in range(time-2):          # leave final day
            date = j + 1
            if (FMA[j] >= SMA[j]) & (FMA[j+1] < SMA[j+1]):  # ie FMA crosses the SMA from above 
                if portfolio[stock] == 0:      # can't sell if you have no stocks
                    pass
                else:
                    proc.sell(date, stock, stock_prices, fees, portfolio, ledger)
            elif (FMA[j] <= SMA[j]) & (FMA[j+1] > SMA[j+1]):
                proc.buy(date, stock, amount, stock_prices, fees, portfolio, ledger)
            else:
                pass   # do nothing option so don't log anything
            
    for stock_no in range(number_of_stocks):  # sell all stocks on final day
        # Note: portfolio can still contain some shares of failed companies at end of day
        date = (time - 1)
        stock = stock_no
        if portfolio[stock] == 0:     # if have no stocks to sell, pass
            pass
        else:
            proc.sell(date, stock, stock_prices, fees, portfolio, ledger)
            
            
def momentum(stock_prices, osc_type='stochastic', n=7, overvalued_bound=0.7, undervalued_bound=0.3, cool_down=3, amount=5000, fees=20, ledger='ledger_momentum.txt'):
    
    
    number_of_stocks = len(stock_prices[0])  # how many stocks we own
    time = len(stock_prices[:,0])            # how many days worth of data
        
    available_amounts = amount / number_of_stocks  # split money evenly
        
    # create portfolio on day 0 with equally split shares
    portfolio = proc.create_portfolio(available_amounts, stock_prices, fees, ledger)
    
    for stock in range(number_of_stocks):
        day = 0
        stock_price = stock_prices[:, stock]

        if osc_type == 'stochastic':
            osc = indic.oscillator(stock_price, n, osc_type='stochastic')

        else: # osc is RSI
            osc = indic.oscillator(stock_price, n, osc_type='RSI')
            
        while day < time - 1:   # ignore data before cool down period since can't have  
                                 # been past threshold for long enough
            
                
            # I attempted a cool down period, but the code is still buggy
            osc_threshold = osc[(day - cool_down + 1) : day + 1]
            osc_period = len(osc_threshold)

            count_under = 0
            count_over = 0

            for j in range(osc_period):
                if osc_threshold[j] > overvalued_bound:   # count how many days in this period it is over
                    count_over += 1                       # the threshold
                elif osc_threshold[j] < undervalued_bound:
                    count_under += 1                      # count the days under
                else:
                    count_over = count_over
                    count_under = count_under

            if count_over == cool_down:        # only act if it is over for all days in this period
                if portfolio[stock] == 0:      # can't sell if you have no stocks
                    day += 1
                else:
                    date = day
                    proc.sell(date, stock, stock_prices, fees, portfolio, ledger)
                    day += cool_down

            elif count_under == cool_down:      # only act if it is under for all days in this period
                date = day
                proc.buy(date, stock, amount, stock_prices, fees, portfolio, ledger)
                count_under = 0
                day += cool_down

            else:
                day += 1    # we only buy/sell if osc beyond threshold for a certain period

        # Note: portfolio can still contain some shares of failed companies at end of day
        date = (time - 1)

        if portfolio[stock] == 0:     # if have no stocks to sell, pass
            pass
        else:
            proc.sell(date, stock, stock_prices, fees, portfolio, ledger)
