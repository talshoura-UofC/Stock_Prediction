# Developed by Tariq Al Shoura
# on the 02 July 2022
# This code will generate the inputs to the CLI to be used in the output code

import csv
import numpy as np

# Getting the data from the file
data = []   
with open('Data.csv', 'r') as file:
    reader = csv.reader(file)
    for row in reader:      # read row by row and append to the data list
        data.append(row)

a, b = np.shape(data)   # obtaining the size of data
print("100", a, "1")
day = 1
for i in range(a):
    print(data[i][0], "0", "".join(data[i][day:day+5]))
