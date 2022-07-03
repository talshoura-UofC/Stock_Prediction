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
print("117.09", a, "46") #675.88
day = 47
owned = [0, 0, 0, 0, 0, 2, 0, 1, 0, 0] #[0, 0, 0, 0, 0, 9, 0, 0, 0, 9]#
for i in range(a):
    print(data[i][0], "{:2d}".format(owned[i]), "".join(data[i][day:day+5]))  #np.max([0,i-3])
