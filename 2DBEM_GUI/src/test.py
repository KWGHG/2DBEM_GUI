import numpy as np

X = np.zeros([3, 2])
file = open("test.dat", "w")

for ix, iy in np.ndindex(X.shape):
    print(X[ix, iy])
