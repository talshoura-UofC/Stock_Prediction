# Developed by Tariq Al Shoura
# on the 02 July 2022
# This code will generate the inputs to the CLI to be used in the output code

import csv
import numpy as np
import subprocess

DEBUG = 0

# Getting the data from the file
data = []   
with open('Data.csv', 'r') as file:
    reader = csv.reader(file)
    for row in reader:      # read row by row and append to the data list
        data.append(row)

# getting the number of stocks and days
DAYS_TO_DISPLAY = 5                   # number of prior days to display in each iteration
numStocks, numData = np.shape(data)   # obtaining the size of data
available_days = 20 #numData - DAYS_TO_DISPLAY - 1    # number of availble days to go throw

currentMoney = 100
selectedStocks = {  # initializing stocks to no ownership and current trading price
    str(data[item][0]): [0, data[item][DAYS_TO_DISPLAY]] for item in range(numStocks)
}
if DEBUG: print(selectedStocks)

for day in range(available_days):
    # preparing the header containing the m, k, d values
    p = subprocess.Popen('python output.py', stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
    headerStr = "{:.4f}".format(currentMoney) + " " + str(numStocks) + " " + str(available_days - day) + "\n"
    if DEBUG: print(headerStr, end = '')

    # preparing the stock data to send
    dataStr = ""
    for i in range(numStocks):     # printing the stocks details
        dataStr = dataStr + str(data[i][0]) + " " + str(selectedStocks[data[i][0]][0]) + " " + "".join(data[i][day+1:day+DAYS_TO_DISPLAY+1]) + "\n"
        selectedStocks[data[i][0]][1] = data[i][day+DAYS_TO_DISPLAY] # updating the stocks prices
    if DEBUG: print(dataStr, end = '')
    if DEBUG: print(selectedStocks)
    
    outStream = headerStr + dataStr
    p.stdin.write(outStream.encode('utf-8'))   # sending the data to output.py as bytes
    out, err = p.communicate()                 # getting the required trades
    decoded_out = out.decode('utf-8').split()  # converting and spliting the results to string
    if DEBUG: print(decoded_out)

    numOperations = int(decoded_out[0])
    for op in range(numOperations):
        if (decoded_out[op*3 + 2] == 'BUY'):
            if (currentMoney > (int(decoded_out[op*3 + 3])*float(selectedStocks[decoded_out[op*3 + 1]][1]))):
                currentMoney = currentMoney - int(decoded_out[op*3 + 3])*float(selectedStocks[decoded_out[op*3 + 1]][1])
                selectedStocks[decoded_out[op*3 + 1]][0] = int(selectedStocks[decoded_out[op*3 + 1]][0]) + int(decoded_out[op*3 + 3])
            # print("buying")



        elif (decoded_out[op*3 + 2] == 'SELL'):
            currentMoney = currentMoney + int(decoded_out[op*3 + 3])*float(selectedStocks[decoded_out[op*3 + 1]][1])
            selectedStocks[decoded_out[op*3 + 1]][0] = int(selectedStocks[decoded_out[op*3 + 1]][0]) - int(decoded_out[op*3 + 3])

            # print("selling")
        else:
            print("error")

    # print(numOperations)
    print(decoded_out)

# print(currentMoney)
# print(selectedStocks)
# selling any remaining stocks
for i in range(numStocks):
    selectedStocks[data[i][0]][1] = data[i][day+DAYS_TO_DISPLAY+1] # updating the stocks prices
    currentMoney = currentMoney + float(selectedStocks[data[i][0]][1])*int(selectedStocks[data[i][0]][0])
    selectedStocks[data[i][0]][0] = 0

print("Finished with $" , currentMoney)
# print(selectedStocks)