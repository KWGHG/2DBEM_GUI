import numpy as np
import math

def translation(X ,tx ,ty):
    matrix = np.array([[1 ,0 ,tx],[0 ,1 ,ty],[0 ,0 ,1]])
    XX = np.zeros([3 ,1])
    XX[0,0] = X[0]
    XX[1,0] = X[1]
    XX[2,0] = 1
    A = matrix.dot(XX)
    A1 = np.zeros(2)
    A1[0] = A[0,0]
    A1[1] = A[1,0]
    return A1

def rotating(X ,theta):
    matrix = np.array([[math.cos(theta) ,-math.sin(theta) ,0],[math.sin(theta) ,math.cos(theta) ,0],[0 ,0 ,1]])
    XX = np.zeros([3 ,1])
    XX[0,0] = X[0]
    XX[1,0] = X[1]
    XX[2,0] = 1
    A = matrix.dot(XX)
    A1 = np.zeros(2)
    A1[0] = A[0,0]
    A1[1] = A[1,0]
    return A1


def scaling(X ,sx ,sy):
    matrix = np.array([[sx ,0 ,0],[0 ,sy ,0],[0 ,0 ,1]])
    XX = np.zeros([3 ,1])
    XX[0,0] = X[0]
    XX[1,0] = X[1]
    XX[2,0] = 1
    A = matrix.dot(XX)
    A1 = np.zeros(2)
    A1[0] = A[0,0]
    A1[1] = A[1,0]
    return A1


#if __name__ == "__main__":
#    X = np.zeros(2)
#    print(translation(X,1,1))
