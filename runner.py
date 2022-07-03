# Developed by Tariq Al Shoura
# on the 02 July 2022
# This code will generate the inputs to the CLI to be used in the output code

import csv
import numpy as np
import subprocess

# Getting the data from the file
data = []   
with open('Data.csv', 'r') as file:
    reader = csv.reader(file)
    for row in reader:      # read row by row and append to the data list
        data.append(row)

# getting the number of stocks and days
DAYS_TO_DISPLAY = 5                     # number of prior days to display in each iteration
num_stocks, num_data = np.shape(data)   # obtaining the size of data
available_days = 3 #num_data - DAYS_TO_DISPLAY     # number of availble days to go throw

for day in range(available_days):
    p = subprocess.Popen('python output.py', stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
    headerStr = "100" + " " + str(num_stocks) + " " + str(available_days - day) + "\n"
    # p.stdin.write(headerStr.encode('utf-8'))
    print(headerStr, end = '')
    # print("100", num_stocks, available_days - day)   # printing each days header

    dataStr = ""
    for i in range(num_stocks):     # printing the stocks details
        dataStr = dataStr + str(data[i][0]) + " " + "0" + " " + "".join(data[i][day+1:day+DAYS_TO_DISPLAY+1]) + "\n"
        # p.stdin.write(headerStr.encode('utf-8'))
    print(dataStr, end = '')
    
    outStream = headerStr + dataStr
    p.stdin.write(outStream.encode('utf-8'))
    out, err = p.communicate()
    print(out.decode('utf-8'))

    
