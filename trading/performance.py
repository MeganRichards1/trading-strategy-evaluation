# Evaluate performance.
import numpy as np
import trading.strategy as strategy
import matplotlib.pyplot as plt

def read_ledger(ledger_file):
    '''
    Reads and reports useful information from ledger_file.
    '''
    # Begin by counting the number of transactions
    count = 0
    for line in open(ledger_file, 'r').readlines(): # open the file and count the number of lines
        count += 1
    
    # Now, create a list such that each entry is a transaction
    file = open(ledger_file, "r")          # opens the file in read mode
    transactions = file.read().split('\n') # puts the file into an array
    file.close()                           # close the file

    all_entries = []
    total_transactions = []
    neg_trans = []
    pos_trans = []
    trans_days = []
    cum_sum = 0
    cum_sum_plot = [0]
    stocks = []
    
    # Now, study the individual transactions
    for i in range(count):
        
        ind_trans = transactions[i]     # get each individual transaction as string from the list
        entries = ind_trans.split(',')  # split the string into individual entries and... put these
        all_entries.append(entries)     # ...into an array with number of rows equal to number of
                                        # transactions, and columns containing corresp entry in ledger
            
        stock_no = all_entries[i][2]
    
        if stock_no not in stocks:
            stocks.append(stock_no)     # gives list of stock numbers as strings
        else:
            pass
    
        no_of_stocks = len(stocks)      # how many stocks we have data for 
        trans_amount = int(float(all_entries[i][5]))  # get the amount (+ve or -ve) of each transaction
        
        cum_sum += trans_amount
        cum_sum_plot.append(cum_sum)
        
        total_transactions.append(trans_amount)       # create list of all amounts
        total_transaction_amount = sum(total_transactions) # get total profit/loss
        
        trans_day = int(all_entries[i][1])
        trans_days.append(trans_day)
        
        # Here, calculate the total spent and earned
        if total_transactions[i] <= 0:
            neg_trans.append(abs(total_transactions[i]))   # list of 'buy' transactions
        else:
            pos_trans.append(total_transactions[i])   # list of 'sell' transactions
        
        # Get sum of each list
        amount_spent = sum(neg_trans)
        amount_earned = sum(pos_trans)
        
        overall = amount_earned - amount_spent
        
    last_day = max(trans_days)  # last day where we sell everything

    end_portfolio = [0]*no_of_stocks
 
    for k in range(count):
        if int(all_entries[k][1]) == last_day:
            stock = int(all_entries[k][2])
            end_portfolio[stock] = int(all_entries[k][3])
        else:
            pass
    
    print(f'The total number of transactions performed was {count}. \nThe total amount spent was {amount_spent}, while the total amount earned was {amount_earned}. \nThe overall profit/loss was {overall}. \nThe portfolio before the sales on the final day was {end_portfolio}.')
    trans_no = list(range(count + 1))  
    plt.figure(figsize=(20,10))
    plt.plot(trans_no, cum_sum_plot)
    plt.grid()
    plt.title('A plot of the amount of money we have over time', fontsize = 20)
    plt.xlabel('Transaction number', fontsize = 20)
    plt.ylabel('Cumulative amount of money we have', fontsize = 20)
    plt.show()