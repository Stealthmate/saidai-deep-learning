import numpy as np
import csv

np.random.seed(0)
X = np.random.normal(35, 10, 100)
A = 1300
B = 10000
Y = A * X + B + np.random.normal(0, 6000, 100)
with open('data.csv', mode='w') as f:
    w = csv.writer(f)
    for r in zip(X, Y):
        w.writerow(r)
