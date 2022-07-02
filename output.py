# Developed by Tariq Al Shoura
# on the 02 July 2022
# This code will read the inputs from the CLI and prints some outputs

import numpy as np

def stock_pred(names, owned, prices, k):
    prices = np.array(prices)
       
    # finding the 1st and 2nd degree polynomial fits
    num_stocks, num_days = np.shape(prices)
    x = np.arange(num_days)+1    
    poly_1d = []; poly_2d = []; p1 = []; p2 = []
    for i in range(num_stocks):
        poly_1d.append(np.polyfit(x, prices[i], 1)) # 1st degree
        poly_2d.append(np.polyfit(x, prices[i], 2)) # 2nd degree
        p1.append(np.poly1d(poly_1d[i])); p2.append(np.poly1d(poly_2d[i]))  # appending

    print(np.shape(p1))
    # print(["{:>9.2f}".format(k) for k in poly_1d[0]])
    # print(["{:>9.2f}".format(k) for k in poly_2d[0]])
    # print(p1[0].c, np.shape(p1[0]), type(p1[0]))
    # print(p2[0].c, np.shape(p2[0]), type(p2[0]))

    print('\n\n')
    trends_1d = np.gradient(prices[0:2], 1, axis=1)
    trends_2d = np.gradient(prices[0:2], 2, axis=1)
    for i in range(2):
        print("items in stock", names[i], "are", ["{:>9.2f}".format(k) for k in prices[i]])
        print("1st deg poly is:", ["{:>9.2f}".format(k) for k in p1[i].c], "\t\t    predected value is:", "{:>9.2f}".format(p1[i](num_days+1)))
        print("2nd deg poly is:", ["{:>9.2f}".format(k) for k in p2[i].c], "   predected value is:", "{:>9.2f}".format(p2[i](num_days+1)))
        print("First digree gradient ", ["{:>9.2f}".format(k) for k in trends_1d[i]])
        print("Second digree gradient", ["{:>9.2f}".format(k) for k in trends_2d[i]], '\n')



        # print("items in stock", names[i], "are", ["{:+08.2f}".format(k) for k in prices[i]])
        # print("First digree gradient ", ["{:+08.2f}".format(k) for k in trends_1d[i]])
        # print("Second digree gradient", ["{:+08.2f}".format(k) for k in trends_2d[i]], '\n')


# Reading the inputs:
    # m - the amount of money you could spend that day.
    # k - the number of different stocks available for buying or selling.
    # d - the number of remaining days for trading stocks.
[m, k, d] = list(map(int, input().split())) # reading the splitting the line into the required variables
# m = int(m); k = int(k); d = int(d);

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
for i in range(k):
    print("items in stock", names[i], "are", prices[i])

stock_pred(names, owned, prices, k)


