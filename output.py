# Developed by Tariq Al Shoura
# on the 02 July 2022
# This code will read the inputs from the CLI and prints some outputs indecating which stocks to buy or sell

# importing  lib
import numpy as np
import math
from pandas import *

# declaring constansts used for debuging and threshold
DEBUG = 0
BUY_THRESHOLD = -4
SELL_THRESHOLD = 1

# function that takes the stock details and outputs which stocks to buy or sell
def stock_pred(names, owned, prices, m, k):
    prices = np.array(prices)   # converting to numpy array

    # finding the 1st to 3rd degree polynomial fits
    numStocks, num_days = np.shape(prices)
    x = np.arange(num_days)+1    
    poly_1d = []; poly_2d = []; poly_3d = []    # will be used to fit the poly
    p1 = []; p2 = []; p3 = []                   # will be used to predict the next value
    for i in range(numStocks):
        poly_1d.append(np.polyfit(x, prices[i], 1)) # 1st degree    // not used anymore
        poly_2d.append(np.polyfit(x, prices[i], 2)) # 2nd degree    // not used
        poly_3d.append(np.polyfit(x, prices[i], 3)) # 3rd degree
        p1.append(np.poly1d(poly_1d[i])); p2.append(np.poly1d(poly_2d[i])); p3.append(np.poly1d(poly_3d[i]))  # appending data to a list

    # calculating gardients between points {was used for information analysis}
    trends_1d = np.gradient(prices[0:numStocks], 1, axis=1)    # first order grad   // not used anymore
    trends_2d = np.gradient(prices[0:numStocks], 2, axis=1)    # second order grad  // not used anymore

    # getting the highest order coefficient for each polynomial
    slops = []; curves = []; curv_3 = []
    for i in range(numStocks):
        slops.append(p1[i].c[0])    # for 1st order
        curves.append(p2[i].c[0])   # for 2nd order
        curv_3.append(p3[i].c[0])   # for 3rd order

        if DEBUG:   # for information analysis
            print("items in stock", names[i], "are", ["{:>9.2f}".format(k) for k in prices[i]])
            print("1st deg poly is:", ["{:>9.2f}".format(k) for k in p1[i].c], "\t\t    predected value is:", "{:>9.2f}".format(p1[i](num_days+1)))
            print("2nd deg poly is:", ["{:>9.2f}".format(k) for k in p2[i].c], "   predected value is:", "{:>9.2f}".format(p2[i](num_days+1)))
            print("3nd deg poly is:", ["{:>9.2f}".format(k) for k in p3[i].c], "   predected value is:", "{:>9.2f}".format(p3[i](num_days+1)))
            print("First digree gradient ", ["{:>9.2f}".format(k) for k in trends_1d[i]])
            print("Second digree gradient", ["{:>9.2f}".format(k) for k in trends_2d[i]])
            print("average predicted value for 2d", "{:>9.2f}".format( (p1[i](num_days+1)+p2[i](num_days+1))/2 ))
            print("average predicted value for 2d", "{:>9.2f}".format( (p1[i](num_days+1)+p2[i](num_days+1)+p3[i](num_days+1))/3 ))
            print("Owned", "{:>9.0f}".format(owned[i]))
            print('\n')
            print("items in stock", names[i], "are", ["{:+08.2f}".format(k) for k in prices[i]])
            print("First digree gradient ", ["{:+08.2f}".format(k) for k in trends_1d[i]])
            print("Second digree gradient", ["{:+08.2f}".format(k) for k in trends_2d[i]], '\n')

    
    # creating a data matrix from information of interest
        # 0: Stock Name, 
        # 1: Current Price, 
        # 2: predicted benifit/loss using 2nd order poly, 
        # 3: predicted benifit/loss using 3nd order poly,
        # 4: ratio of {2}/Current Price, 
        # 5: ratio of {3}/Current Price,
        # 6: highest coef. in 1st degree fit, 
        # 7: highest coef. in 1st degree fit, 
        # 8: highest coef. in 1st degree fit,
        # 9: number of owned shares
    dataAnalysis = []
    dataAnalysis.append([k for k in names]) # stock name
    dataAnalysis.append([prices[k,-1] for k in range(numStocks)])  # stock current price
    dataAnalysis.append([((p1[k](num_days+1)+p2[k](num_days+1))/2) - prices[k,-1] for k in range(numStocks)])    # predicted price difference in 2d
    dataAnalysis.append([((p1[k](num_days+1)+p2[k](num_days+1)+p3[k](num_days+1))/3) - prices[k,-1] for k in range(numStocks)])    # predicted price difference in 3d
    dataAnalysis.append([(((p1[k](num_days+1)+p2[k](num_days+1))/2) - prices[k,-1])/prices[k,-1]*100 for k in range(numStocks)])   # ratio of prediction in 2d
    dataAnalysis.append([(((p1[k](num_days+1)+p2[k](num_days+1)+p3[k](num_days+1))/3) - prices[k,-1])/prices[k,-1]*100 for k in range(numStocks)]) # ratio of prediction in 2d
    dataAnalysis.append([k for k in slops])     # first degree fit
    dataAnalysis.append([k for k in curves])    # second degree fit 
    dataAnalysis.append([k for k in curv_3])    # third  degree fit
    dataAnalysis.append([k for k in owned])     # stock name

    # transposing the data and creating a dataframe
    transposedData = np.asarray(dataAnalysis, dtype=object).T.tolist()
    dataframe = pandas.DataFrame(transposedData)


# BUYING STOCKS {maybe make it a function later}
    # selecting stocks that (can be purchesed given the available money) and (has a third order prediction ratio < buying thershold)
    obtainableStocks = (dataframe.loc[dataframe[1] < m].loc[dataframe[5] < BUY_THRESHOLD]).sort_values(by=5, ascending=False)
    if DEBUG: print("\n\nobtainableStock"); print(obtainableStocks); print("\n\n")

    # bulk buying favourable stocks if possible
    numOfBuyStock  = np.shape(obtainableStocks)[0]
    if DEBUG: print("money", m, 'obtainableStocks total', np.sum(obtainableStocks[1]))
    if numOfBuyStock > 0:   # if there are any desirable stocks
        BulkBuy = math.floor(m/np.sum(obtainableStocks[1])) # number of possible bulk buys for all desired stocks
        if DEBUG: print("BulkBuy", BulkBuy)
        requiredBuys = np.ones(numOfBuyStock)*BulkBuy   # updating the buying list
        m = m - BulkBuy*np.sum(obtainableStocks[1])     # updating the available money
        if DEBUG: print(m, requiredBuys)

        # buying with any remaining money
        purchase = 1
        while (purchase > 0):   # while purchesing is still occuring
            purchase = 0
            for i in range(numOfBuyStock):
                if (m >= obtainableStocks.iat[i,1]):           # if a stock can be bought
                    requiredBuys[i] = requiredBuys[i] + 1      # buy a stock
                    m = m-obtainableStocks.iat[i,1]            # adjusting remaining money
                    purchase = 1                               # indecate a purchase has occured
        if DEBUG: print(requiredBuys)
    
    else:  # set buying list to zero
        requiredBuys = 0
    


# SELLING STOCKS {maybe make it a function later}
    # selecting stocks that (are owned) and (has a third order prediction ratio > selling thershold)
    sellableStocks = (dataframe.loc[dataframe[9] > 0].loc[dataframe[5] >= SELL_THRESHOLD]).sort_values(by=9, ascending=False)
    if DEBUG: print("\nsellableStocks"); print(sellableStocks); print("\n\n")
    numOfSellStock  = np.shape(sellableStocks)[0]   # indecate a stock to be sold


    # Print required transactions
    numTransactions = np.count_nonzero(numOfBuyStock) + numOfSellStock
    print(numTransactions)
    for i in range(numOfBuyStock):
        if requiredBuys[i] > 0:
            print(obtainableStocks.iat[i,0], 'BUY', int(requiredBuys[i]))   # printing stocks to buy
    for i in range(numOfSellStock):
        print(sellableStocks.iat[i,0], 'SELL', int(sellableStocks.iat[i,9])) # printing stocks to sell





## MAIN CODE

# Reading the inputs:
    # m - the amount of money you could spend that day.
    # k - the number of different stocks available for buying or selling.
    # d - the number of remaining days for trading stocks.
m, k, d = input().split() # reading the splitting the line into the required variables
m = float(m); k = int(k); d = int(d)

# Reading k lines for the stocks
    # name - the name of the stock (a string).
    # owned - the number of shares you own of that stock.
    # prices - 5 space separated numbers representing the stock's price for the last 5 days. 
    #          These are ordered from oldest to newest, so the last number is the current stock price.
names = []; owned = []; prices = [] # init variables

for data in range(k):
    item = input().split()  # reading the splitting the line into list items
    names.append(item[0])
    owned.append(int(item[1]))  # casting to int
    prices.append(list(map(float,item[2:])))    # casting to float

# calling a function to predict stocks
stock_pred(names, owned, prices, m, k)

