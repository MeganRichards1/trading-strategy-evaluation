import numpy as np

def moving_average(stock_price, n=7, weights=[]):
    '''
    Calculates the n-day (possibly weighted) moving average for a given stock over time.

    Input:
        stock_price (ndarray): single column with the share prices over time for one stock,
            up to the current day.
        n (int, default 7): period of the moving average (in days).
        weights (list, default []): must be of length n if specified. Indicates the weights
            to use for the weighted average. If empty, return a non-weighted average.

    Output:
        ma (ndarray): the n-day (possibly weighted) moving average of the share price over time.
    '''
    
    
    # stock_price is one column of the data ie has np.shape (days, ) 
    # where days is how many days worth of data we have 

    time = len(stock_price) # get the number of days over which we have data specified
    weight_length = len(weights)
    
    if (weight_length == 0) == False: # if there are weights specified...
        for i in range(weight_length):
            stock_price[-i] *= weights[i] # ... multiply the stock prices over previous n days 
                                            # by the weights
    else:
        stock_price = stock_price
    
    # Now have the stock prices with the weights taken into account
    # If we don't have enough data, add current av as extra data and print message to explain
    if n > time:
    
        extra_days = n - time # get how many extra days we need data for 
        stock_list = list(stock_price) # create list of stock prices 
        for m in range(1, extra_days):
            current_av = np.mean(stock_price) # calculate average of all given prices
            stock_list.append(current_av)        # add the current average to list
            
        stock_price = np.array(stock_list)
        print('Note: Stock price data adjusted so we have enough data.')
            
    else:
        stock_price = stock_price
    
    # Now we have enough data to calculate moving average
    # Initialise output
    ma = np.zeros(time)
    
    for j in range(n-1):   # for the first few entries, calculate average with 
                           # period smaller than n to get a result
        av = round(np.mean(stock_price[0:j+1]),2)
        ma[j] = av
    for k in range(n-1, time):
        av = round(np.mean(stock_price[k-(n-1):k+1]),2)
        ma[k] = av
    
    return ma

        

def oscillator(stock_price, n=7, osc_type='stochastic'):
    '''
    Calculates the level of the stochastic or RSI oscillator with a period of n days.

    Input:
        stock_price (ndarray): single column with the share prices over time for one stock,
            up to the current day.
        n (int, default 7): period of the moving average (in days).
        osc_type (str, default 'stochastic'): either 'stochastic' or 'RSI' to choose an oscillator.

    Output:
        osc (ndarray): the oscillator level with period $n$ for the stock over time.
    '''
    
    # get the number of days over which we have data specified
    time = len(stock_price) 
    # initialise the output
    osc = np.zeros(time)
    
    if osc_type == 'stochastic':

        for i in range(time):
            todays_price = stock_price[i]
            if i >= n-1:
                max_price = max(stock_price[(i - n + 1):(i + 1)]) # the n days include the current day
                min_price = min(stock_price[(i - n + 1):(i + 1)]) 

            else: # the period asks for more info than you have so...
                # ... set the period to include all the information you have up to this date
                max_price = max(stock_price[:(i + 1)]) # we include the current day
                min_price = min(stock_price[:(i + 1)]) 

            delta = todays_price - min_price
            delta_max = max_price - min_price

            # set to zero avoid zero division error as delta_max = 0 implies delta = 0 
            if delta_max == 0: 
                ratio = np.nan # undefined as stock price constant for this period
            else:
                ratio = delta / delta_max

            osc[i] = ratio
        
    else:
      
        for j in range(time):
            if j >= n-1:
                req_range = stock_price[(j - n + 1):(j + 1)]   # include current day

            else: # the period asks for more info than you have so...
                # ... set the period to include all the information you have up to this date
                req_range = stock_price[:(j + 1)] # need extra day before in the range
            
            # we adjusted the period when we didn't have enough data
            # therefore get the new periods
            range_len = len(req_range)

            pos_diff = []
            neg_diff = []

            for k in range(1, range_len): # loop over the data from the last n days
                difference = req_range[k] - req_range[k-1]
                if difference > 0:
                    pos_diff.append(difference)
                elif difference < 0:
                    neg_diff.append(difference)
                else:   # if difference = 0, we discard the value
                    pass

            if neg_diff ==[] and pos_diff == []: # constant stock price throughout...
                RSI = np.nan                     # ... set as undefined

            elif neg_diff ==[]:           # ie no negative differences
                RSI = 1                   # since RS tends to inf so RSI tends to 1
                
            elif pos_diff ==[]:           # ie no positive differences
                RSI = 0                   # since RS is 0 and RSI is also 0

            else:
                av_pos_diff = np.mean(pos_diff)       # returns nan if either list is empty
                av_neg_diff = abs(np.mean(neg_diff))  # which is what we want
                if (av_pos_diff is np.nan) or (av_neg_diff is np.nan):
                    RSI = np.nan      # undefined if either list empty as can't get a ratio
                else:
                    RS = av_pos_diff / av_neg_diff
                    RSI = 1 - (1 / (1 + RS))

            osc[j] = RSI
        
    
    return osc