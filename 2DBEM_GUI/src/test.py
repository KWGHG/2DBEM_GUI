import numpy as np

if __name__ == "__main__":
    Temp = np.append(
        np.logspace( 1 ,5 ,5 ,base=0.2),
        np.linspace(0 ,1 ,5))
    print(Temp)