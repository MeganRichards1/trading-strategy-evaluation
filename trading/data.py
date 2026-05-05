# Lines 128 to 141: unutbu
# URL: https://stackoverflow.com/questions/2566412/find-nearest-value-in-numpy-array
# Accessed on 12 Nov 2020.

import numpy as np

# Make a function for the news
def news(volatility):
    '''
    Decides whether there is news or not, and hence returns a list of the 
    corresponding drift (a list of zeros if there is no news).
    
    Input: 
        volatility (int): volatility of the stock of a given company 
    
    Output: 
        ind_drift (list): list of one drift value with length equal to duration of drift
    '''
    # Set up the default_rng from Numpy
    rng = np.random.default_rng()
    
    # Randomly choose the duration between 3 and 14 days
    duration = rng.integers(3,15)
    
    # Generate 1D array containing either 0 (prob 0.9) or 1 (prob 0.1)
    news_today = rng.choice(2, 1, p = [0.1, 0.9]) 
    
    # If '1' returned, there is news. Otherwise, there is no news.
    if news_today[0] == 1:
        
        # Calculate m and drift
        m = rng.normal(0,2)
        drift = m * volatility
        
        # Initialise the list corresponding to drift with length duration
        ind_drift = np.zeros(duration)
        
        # Add drift value to each entry 
        for day in range(duration):
            ind_drift[day] = drift
        return ind_drift
    
    else:
        # there is no news, so list of zeros returned
        ind_drift =  np.zeros(duration)
        return ind_drift
    

def generate_stock_price(days=1000, initial_price=None, volatility=None):
    '''
    Generates daily closing share prices for a company,
    for a given number of days.
    
    Input: 
        days (int): number of days you want to generate stock price data for (default 1000).
        
        initial_price (list): list of initial prices for each stock (default None).
        
        volatility (list): list of volatilities for each stock (default None).
    Output:
        gen_data (ndarray): NumPy array with N columns, containing the price data
            for the required N stocks each day over the number of days specified.
        
    '''
    # Calculate number of stocks from values specified
    number_of_stocks = len(initial_price)
    
    # Initialise output array
    stock_price_array = np.zeros((number_of_stocks, days))
    
    # Generate stock price data for each stock individually
    for stock in range(number_of_stocks):  # loop over number of stocks
        
        # Get initial price and volatility of each stock
        p0 = initial_price[stock]
        v = volatility[stock]
        
        # Construct random number class Generator
        rng = np.random.default_rng()
        
        # Initialise stock_prices to be a list of length 'days'
        stock_prices = np.zeros(days)
        
        # Set first entry to be initial price of the stock
        stock_prices[0] = p0
        
        # Initialise list of length 'days' to hold the total drift for each day
        totalDrift= np.zeros(days)
        
        # Loop over all days excluding the first (which has the inputted price)
        for day in range(1, days):
            
            # Get the random normal increment
            inc = rng.normal(0, v)
            
            # Add stock_prices[day-1] to inc to get NewPriceToday
            NewPriceToday = stock_prices[day-1] + inc
            
            # Get the drift from the news
            d = news(v)
            
            # Get the duration
            duration = len(d)
            
            # Add the drift to the next days 
            for time in range(duration):
                if days < day + duration:
                    totalDrift[day+time-1:days-1] = d[time]
                else:
                    totalDrift[day+time-1] = d[time]
                    
            # Add today's drift to today's price
            NewPriceToday += totalDrift[day]
            
            # Set stock_prices[day] to NewPriceToday or to NaN if it's negative
            if NewPriceToday <=0:
                stock_prices[day:] = np.nan
            else:
                stock_prices[day] = NewPriceToday
            
        stock_price_array[stock] = stock_prices   
    gen_data = stock_price_array.T   # need to transpose the array to get the desired output format
        
    return gen_data

# Create a function that compares an array to a value and returns closest match in array
# Needed to find closest values of initial price and volatility in the stock data
def find_nearest(array, value):
    ''' Returns the entry in an array that is closest to a specified value. 
    
    Input:
        array (ndarray): the array you are comparing the value to.
        
        value (int): the value you are matching the list to.
        
    Output: 
        match (int): the value in the list that is closest to the given value.    
    '''
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return array[idx]

def get_data(method='read', initial_price=None, volatility=None):
    '''
    Generates or reads simulation data for one or more stocks over 5 years,
    given their initial share price and volatility.
    
    Input:
        method (str): either 'generate' or 'read' (default 'read').
            If method is 'generate', use generate_stock_price() to generate
                the data from scratch.
            If method is 'read', use Numpy's loadtxt() to read the data
                from the file stock_data_5y.txt.
            
        initial_price (list): list of initial prices for each stock (default None)
            If method is 'generate', use these initial prices to generate the data.
            If method is 'read', choose the column in stock_data_5y.txt with the closest
                starting price to each value in the list, and display an appropriate message.
        
        volatility (list): list of volatilities for each stock (default None).
            If method is 'generate', use these volatilities to generate the data.
            If method is 'read', choose the column in stock_data_5y.txt with the closest
                volatility to each value in the list, and display an appropriate message.

        If no arguments are specified, read price data from the whole file.
        
    Output:
        sim_data (ndarray): NumPy array with N columns, containing the price data
            for the required N stocks each day over 5 years.
    
    Examples:
        Returns an array with 2 columns:
            >>> get_data(method='generate', initial_price=[150, 250], volatility=[1.8, 3.2])
            
        Displays a message and returns None:
            >>> get_data(method='generate', initial_price=[150, 200])
            Please specify the volatility for each stock.
            
        Displays a message and returns None:
            >>> get_data(method='generate', volatility=[3])
            Please specify the initial price for each stock.
        
        Returns an array with 2 columns and displays a message:
            >>> get_data(method='read', initial_price=[210, 58])
            Found data with initial prices [210, 100] and volatilities [1.2, 3.4].
        
        Returns an array with 1 column and displays a message:
            >>> get_data(volatility=[5.1])
            Found data with initial prices [380] and volatilities [5.2].
        
        If method is 'read' and both initial_price and volatility are specified,
        volatility will be ignored (a message is displayed to indicate this):
            >>> get_data(initial_price=[210, 58], volatility=[5, 7])
            Found data with initial prices [210, 100] and volatilities [1.2, 3.4].
            Input argument volatility ignored.
    
        No arguments specified, all default values, returns price data for all stocks in the file:
            >>> get_data()
            '''
    # begin by getting info
     # corresponds to doc string - want no. of stocks inputted
    
    if method == 'read':
        stock_data = np.loadtxt('stock_data_5y.txt')
        M = len(stock_data[1:,1]) # move this outside of if? this is no. of entries
        init_read_data = stock_data[1] # get initial stock prices from text file
        volatility_read_data = stock_data[0] # first row corresponds to volatility
        
        if initial_price == None:
            
            if volatility == None:
                print(f'Price data for all stocks returned, with initial prices {init_read_data} and volatilities {volatility_read_data}')
                sim_data = stock_data[1:, :]
                return sim_data
            
            else:
                N = len(volatility)
                sim_data = np.zeros((M,N)) # initialise
                
                matched_vol = []
                matched_prices = []
                indices = []
                for i in range(N):
                    value = volatility[i]
                    match = find_nearest(volatility_read_data, value)
                    matched_vol.append(match) # matched data returns the matched stocks
                for k in range(N):
                    for j in range(20):
                        if volatility_read_data[j] == matched_vol[k]:
                            indices.append(j)
                            matched_prices.append(init_read_data[j])
                        else:
                            matched_vol = matched_vol
                for l in range(N):
                    sim_data[:, l] = stock_data[1:, indices[l]] # jth column
                print(f'Found data with initial prices {matched_prices} and volatilities {matched_vol}.')
                return sim_data
        
        elif type(initial_price) == list:
            N = len(initial_price)
            sim_data = np.zeros((M,N)) # initialise
            
            matched_prices = []
            matched_vol = []
            indices = []
            for i in range(N):
                value = initial_price[i]
                match = find_nearest(init_read_data, value)
                matched_prices.append(match)
            for k in range(N):
                for j in range(20):
                    if init_read_data[j] == matched_prices[k]:
                        indices.append(j)
                        matched_vol.append(volatility_read_data[j])
                    else:
                        matched_vol = matched_vol
            for l in range(N):
                sim_data[:, l] = stock_data[1:, indices[l]] # jth column
            if type(volatility) == list:
                    print(f'Found data with initial prices {matched_prices} and volatilities {matched_vol}. Input argument volatility ignored.')
                    return sim_data
            else:
                    print(f'Found data with initial prices {matched_prices} and volatilities {matched_vol}.')
                    return sim_data
        
        else:
            print('Please input the initial price for each stock as a list.')
            
    else:
        # method is generate
        if initial_price == None:
            print('Please specify the initial price for each stock.')
            return None
        elif volatility == None: 
            print('Please specify the volatility for each stock.')
            return None
        else:
            five_years = 5 * 365
            N = len(initial_price)
            sim_data = generate_stock_price(five_years, initial_price, volatility)# stock price at end of that day
            return sim_data