# Developed by Tariq Al Shoura
# on the 02 July 2022
# This code will read the inputs from the CLI and prints some outputs

import numpy as np
import math
from pandas import *
DEBUG = 0


def stock_pred(names, owned, prices, m, k):
    prices = np.array(prices)
       
    # finding the 1st and 2nd degree polynomial fits
    numStocks, num_days = np.shape(prices)
    x = np.arange(num_days)+1    
    poly_1d = []; poly_2d = []; poly_3d = []
    p1 = []; p2 = []; p3 = []
    for i in range(numStocks):
        poly_1d.append(np.polyfit(x, prices[i], 1)) # 1st degree
        poly_2d.append(np.polyfit(x, prices[i], 2)) # 2nd degree
        poly_3d.append(np.polyfit(x, prices[i], 3)) # 3rd degree
        p1.append(np.poly1d(poly_1d[i])); p2.append(np.poly1d(poly_2d[i])); p3.append(np.poly1d(poly_3d[i]))  # appending

    # print(np.shape(p1))
    # print(["{:>9.2f}".format(k) for k in poly_1d[0]])
    # print(["{:>9.2f}".format(k) for k in poly_2d[0]])
    # print(p1[0].c, np.shape(p1[0]), type(p1[0]))
    # print(p2[0].c, np.shape(p2[0]), type(p2[0]))

    # calculating gardients between points
    trends_1d = np.gradient(prices[0:numStocks], 1, axis=1)    # first order grad
    trends_2d = np.gradient(prices[0:numStocks], 2, axis=1)    # second order grad

    slops = []; curves = []; curv_3 = []
    for i in range(numStocks):
        if DEBUG:
            print("items in stock", names[i], "are", ["{:>9.2f}".format(k) for k in prices[i]])
            print("1st deg poly is:", ["{:>9.2f}".format(k) for k in p1[i].c], "\t\t    predected value is:", "{:>9.2f}".format(p1[i](num_days+1)))
            print("2nd deg poly is:", ["{:>9.2f}".format(k) for k in p2[i].c], "   predected value is:", "{:>9.2f}".format(p2[i](num_days+1)))
            print("3nd deg poly is:", ["{:>9.2f}".format(k) for k in p3[i].c], "   predected value is:", "{:>9.2f}".format(p3[i](num_days+1)))
            print("First digree gradient ", ["{:>9.2f}".format(k) for k in trends_1d[i]])
            print("Second digree gradient", ["{:>9.2f}".format(k) for k in trends_2d[i]])
            print("average predicted value for 2d", "{:>9.2f}".format( (p1[i](num_days+1)+p2[i](num_days+1))/2 ))
            print("average predicted value for 2d", "{:>9.2f}".format( (p1[i](num_days+1)+p2[i](num_days+1)+p3[i](num_days+1))/3 ))
            print('\n')
            # print("items in stock", names[i], "are", ["{:+08.2f}".format(k) for k in prices[i]])
            # print("First digree gradient ", ["{:+08.2f}".format(k) for k in trends_1d[i]])
            # print("Second digree gradient", ["{:+08.2f}".format(k) for k in trends_2d[i]], '\n')
        slops.append(p1[i].c[0])
        curves.append(p2[i].c[0])
        curv_3.append(p3[i].c[0])

    if DEBUG: 
        print("Stock:", [k.rjust(7) for k in names])
        print("Price:", ["{:>+7.2f}".format(prices[k,-1] ) for k in range(numStocks)])
        print("Pred2:", ["{:>+7.2f}".format( ((p1[k](num_days+1)+p2[k](num_days+1))/2) - prices[k,-1] ) for k in range(numStocks)])
        print("Pred3:", ["{:>+7.2f}".format( ((p1[k](num_days+1)+p2[k](num_days+1)+p3[k](num_days+1))/3) - prices[k,-1] ) for k in range(numStocks)])
        print("Rat2D:", ["{:>+7.2f}".format( (((p1[k](num_days+1)+p2[k](num_days+1))/2) - prices[k,-1])/prices[k,-1]*100 ) for k in range(numStocks)])
        print("Rat3D:", ["{:>+7.2f}".format( (((p1[k](num_days+1)+p2[k](num_days+1)+p3[k](num_days+1))/3) - prices[k,-1])/prices[k,-1]*100 ) for k in range(numStocks)])
        print("Slope:", ["{:>+7.2f}".format(k) for k in slops])
        print("Curve:", ["{:>+7.2f}".format(k) for k in curves])
        print("Cur3D:", ["{:>+7.2f}".format(k) for k in curv_3])
        
    dataAnalysis = []
    dataAnalysis.append([k for k in names]) # stock name
    dataAnalysis.append([prices[k,-1] for k in range(numStocks)])  # stock current price
    dataAnalysis.append([((p1[k](num_days+1)+p2[k](num_days+1))/2) - prices[k,-1] for k in range(numStocks)])    # predicted price difference in 2d
    dataAnalysis.append([((p1[k](num_days+1)+p2[k](num_days+1)+p3[k](num_days+1))/3) - prices[k,-1] for k in range(numStocks)])    # predicted price difference in 3d
    dataAnalysis.append([(((p1[k](num_days+1)+p2[k](num_days+1))/2) - prices[k,-1])/prices[k,-1]*100 for k in range(numStocks)])   # ratio of prediction in 2d
    dataAnalysis.append([(((p1[k](num_days+1)+p2[k](num_days+1)+p3[k](num_days+1))/3) - prices[k,-1])/prices[k,-1]*100 for k in range(numStocks)]) # ratio of prediction in 2d
    dataAnalysis.append([k for k in slops])     # first degree fit slope
    dataAnalysis.append([k for k in curves])    # second // fit 
    dataAnalysis.append([k for k in curv_3])    # third  // fit

    temp = np.asarray(dataAnalysis, dtype=object).T.tolist()
    byPrice = sorted(temp, key=lambda x:float(x[1])) # sorting the items by current prices    
    if DEBUG: pandas.set_option("display.precision", 5); print(DataFrame(byPrice))
    
    cutoff = -1
    for i in range(numStocks):
        if byPrice[i][1] > m:
            cutoff = i
            break
    
    if cutoff > 0:
        possibleBuys = sorted(byPrice[0:cutoff], key=lambda x:float(x[3])) # sort by largest possible loss ratio
        requiredBuys = np.zeros(cutoff) # to store which stocks to buy
        if DEBUG: print(DataFrame(possibleBuys))
        while (m>=possibleBuys[0][1]):  # while there is money to spend
            for i in range(cutoff):
                if (m>=possibleBuys[i][1] and possibleBuys[i][5] < 0):  # if the predected value is a loss
                    requiredBuys[i] = requiredBuys[i] + 1   # buy a stock
                    m = m-possibleBuys[i][1]    # adjusting remaining money
        if DEBUG:  print(requiredBuys)
    
        print(np.count_nonzero(requiredBuys))
        for i in range(cutoff):
            if requiredBuys[i] > 0:
                print(possibleBuys[i][0], 'BUY', int(requiredBuys[i]))
    else:
        print("0")


    # print(DataFrame(dataAnalysis))




# Reading the inputs:
    # m - the amount of money you could spend that day.
    # k - the number of different stocks available for buying or selling.
    # d - the number of remaining days for trading stocks.
m, k, d = input().split() # reading the splitting the line into the required variables
m = float(m); k = int(k); d = int(d);

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
    
# reading the current day, the inputs will be called day by day thus no need to keep track
if DEBUG:
    for i in range(k):
        print("items in stock", names[i], "are", prices[i])
    print('\n\n')

stock_pred(names, owned, prices, m, k)


