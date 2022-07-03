# Developed by Tariq Al Shoura
# on the 02 July 2022
# This code will read the inputs from the CLI and prints some outputs

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
    
for lines in range(d):
    for i in range(k):
        print("items in stock", names[i], "are", prices[i])
