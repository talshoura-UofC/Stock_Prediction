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
for i in range(a):
    print(data[i][0], "0", "".join(data[i][1:6]))



# print("100 2 10")
# print("A 10 4.54 5.53 6.56 5.54 7.60")
# print("B 0 30.54 27.53 24.42 20.11 17.50")

