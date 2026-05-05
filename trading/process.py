# Functions to process transactions.
import numpy as np

def log_transaction(transaction_type, date, stock, number_of_shares, price, fees, ledger_file):
    '''
    Record a transaction in the file ledger_file. If the file doesn't exist, create it.

    Input:
        transaction_type (str): 'buy' or 'sell'
        date (int): the date of the transaction (nb of days since day 0)
        stock (int): the stock we buy or sell (the column index in the data array)
        number_of_shares (int): the number of shares bought or sold
        price (float): the price of a share at the time of the transaction
        fees (float): transaction fees (fixed amount per transaction, independent of the number of shares)
        ledger_file (str): path to the ledger file

    Output: returns None.
        Writes one line in the ledger file to record a transaction with the input information.
        This should also include the total amount of money spent (negative) or earned (positive)
        in the transaction, including fees, at the end of the line.
        All amounts should be reported with 2 decimal digits.

    Example:
        Log a purchase of 10 shares for stock number 2, on day 5. Share price is 100, fees are 50.
        Writes the following line in 'ledger.txt':
        buy,5,2,10,100.00,-1050.00
            >>> log_transaction('buy', 5, 2, 10, 100, 50, 'ledger.txt')
    '''
    total_price = number_of_shares * price  # price is per share
    ledger = open(ledger_file,'a')          # need to delete ledger between runs
    
    if transaction_type == 'buy':
        money_spent = - total_price - fees
        transaction = transaction_type + ', ' + str(date) + ', ' + str(stock) + ', ' + str(number_of_shares) + ', ' + '{0:.2f}'.format(price) + ',' + '{0:.2f}'.format(money_spent)
        ledger.write(transaction + '\n')    # need to start new line w each transaction

    else: # transaction is sell
        money_earned = total_price - fees   # fees are still a negative cose
        transaction = transaction_type + ', ' + str(date) + ', ' + str(stock) + ', ' + str(number_of_shares) + ', ' + '{0:.2f}'.format(price) + ', ' + '{0:.2f}'.format(money_earned)
        ledger.write(transaction + '\n')
        
    ledger.close() # don't forget to close file




def buy(date, stock, available_capital, stock_prices, fees, portfolio, ledger_file):
    '''
    Buy shares of a given stock, with a certain amount of money available.
    Updates portfolio in-place, logs transaction in ledger.

    Input:
        date (int): the date of the transaction (nb of days since day 0)
        stock (int): the stock we want to buy
        available_capital (float): the total (maximum) amount to spend,
            this must also cover fees
        stock_prices (ndarray): the stock price data
        fees (float): total transaction fees (fixed amount per transaction)
        portfolio (list): our current portfolio
        ledger_file (str): path to the ledger file

    Output: None

    Example:
        Spend at most 1000 to buy shares of stock 7 on day 21, with fees 30:
            >>> buy(21, 7, 1000, sim_data, 30, portfolio)
    '''
    price_on_day = stock_prices[date, stock]
    if np.isnan(price_on_day) == True:    # company has failed

        # can't buy anymore stock - remain on the same number of stock
        # and have transaction type 'failed' to indicate no transaction possible
        ledger = open(ledger_file,'a')
        
        transaction = 'failed' + ', ' + str(date) + ', ' + str(stock) + ', ' + str(int(portfolio[stock])) + ' , nan, 0'
        ledger.write(transaction + '\n')  # note: no fees as no transaction occurs
        
        ledger.close()


    else:
        number_of_shares = 1 # start by seeing if we can afford 1 share
        max_shares = 0       # incase can't afford any shares
        
        # establish how much money we have and how much we need
        available_minus_fees = available_capital - fees  # money to spend excl fees
        money_required = number_of_shares * price_on_day
        
        while money_required <= available_minus_fees:
            max_shares = int(number_of_shares)
            number_of_shares += 1
            money_required = number_of_shares * price_on_day + fees

        # Update the list portfolio
        portfolio[stock] += max_shares

        # log the transaction
        if max_shares > 0:
            log_transaction('buy', date, stock, max_shares, price_on_day, fees, ledger_file)
        else:
            pass       # if we can't afford to buy stocks, we don't want to spend fees


def sell(date, stock, stock_prices, fees, portfolio, ledger_file):
    '''
    Sell all shares of a given stock.
    Updates portfolio in-place, logs transaction in ledger.

    Input:
        date (int): the date of the transaction (nb of days since day 0)
        stock (int): the stock we want to sell
        stock_prices (ndarray): the stock price data
        fees (float): transaction fees (fixed amount per transaction)
        portfolio (list): our current portfolio
        ledger_file (str): path to the ledger file

    Output: None

    Example:
        To sell all our shares of stock 1 on day 8, with fees 20:
            >>> sell(8, 1, sim_data, 20, portfolio)
    '''
    available_stock = int(portfolio[stock])  # see how many stocks we have currently to sell
    price_on_day = stock_prices[date, stock] # get the stock price on this day

    if np.isnan(price_on_day) == True:    # company has failed

        # can't buy anymore stock - remain on the same number of stock
        # and have transaction type 'failed' to indicate no sale possible
        ledger = open(ledger_file,'a')
        
        transaction = 'failed' + ', ' + str(date) + ', ' + str(stock) + ', ' + str(int(portfolio[stock])) + ' , nan, 0'
        ledger.write(transaction + '\n') # note: no fees as no transaction occurs
        
        ledger.close()     # don't forget to close file!


    else:
        money_made = price_on_day * available_stock

        # update portfolio
        portfolio[stock] = 0

        # log the transaction
        log_transaction('sell', date, stock, available_stock, price_on_day, fees, ledger_file)



def create_portfolio(available_amounts, stock_prices, fees, ledger_file):
    '''
    Create a portfolio by buying a given number of shares of each stock.

    Input:
        available_amounts (list): how much money we allocate to the initial
            purchase for each stock (this should cover fees)
        stock_prices (ndarray): the stock price data
        fees (float): transaction fees (fixed amount per transaction)
        ledger_file (str): path to the ledger file

    Output:
        portfolio (list): our initial portfolio

    Example:
        Spend 1000 for each stock (including 40 fees for each purchase):
        >>> N = sim_data.shape[1]
        >>> portfolio = create_portfolio([1000] * N, sim_data, 40, 'ledger.txt')
    '''
    # calculate size of portfolio
    N = stock_prices.shape[1]

    # initialise portfolio
    portfolio = np.zeros(N)

    # loop over the stocks
    for i in range(N):
        buy(0, i, available_amounts, stock_prices, fees, portfolio, ledger_file)

    return portfolio