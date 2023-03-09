from scipy import interpolate
import math
import numpy as np

def parametric_airfoil(filename, numbers_of_panel):
    row = 0
    file = open(filename)
    lines = file.readlines()
    for line in lines:
        row += 1
    file.close()

    file = open(filename)
    data = np.empty((row, 2))
    lines = file.readlines()
    row = 0
    upperrow = 0
    for line in lines:
        list1 = line.strip().split()
        data[row, :] = list1[:]
        if data[row,0] == 0:
            upperrow = row
        row += 1
    file.close()
    lowersurfaceX = np.flip(data[0 : int(upperrow + 1), 0])
    lowersurfaceY = np.flip(data[0 : int(upperrow + 1), 1])
    uppersurfaceX = data[int(upperrow) : int(row), 0]
    uppersurfaceY = data[int(upperrow) : int(row), 1]
    #print('lowersurfaceX: ',lowersurfaceX)
    #print('uppersurfaceX: ',uppersurfaceX)
    lowersurface_interpolate_function = interpolate.CubicSpline(
        lowersurfaceX, lowersurfaceY
    )
    uppersurface_interpolate_function = interpolate.CubicSpline(
        uppersurfaceX, uppersurfaceY
    )

    lowersurface_panel = int(numbers_of_panel / 2 )
    uppersurface_panel = int(numbers_of_panel / 2 )

    

    #Temp = np.append(
    #    np.linspace(1 ,0.9 ,int(lowersurface_panel * 0.3)),
    #    np.linspace(0.8999999 ,0.02 ,int(lowersurface_panel * 0.3)),
    #)

    #new_lowersurfaceX = np.append(
    #    Temp,
    #    #np.logspace(1 ,10 ,int(lowersurface_panel * 0.4) ,base=0.2),
    #    np.linspace(0.019999,0,10)
    #)
    Temp = np.linspace(0 ,math.pi ,lowersurface_panel)
    new_lowersurfaceX = np.zeros(lowersurface_panel)
    for i in range(lowersurface_panel):
        new_lowersurfaceX[i] = 0.5 + 0.5 * math.cos(Temp[i] )
        #print(new_lowersurfaceX[i])
    
    new_lowersurfaceY = lowersurface_interpolate_function(new_lowersurfaceX)

    #Temp = np.append(
    #    #np.logspace(10, 1, int(uppersurface_panel * 0.4) ,base=0.2),
    #    np.linspace(0,0.01,10),
    #    np.linspace(0.010001, 0.9, int(uppersurface_panel * 0.3)),
    #)

    #new_uppersurfaceX = np.append(
    #    Temp,
    #    np.linspace(0.9001, 1, int(uppersurface_panel * 0.3))
    #).

    Temp = np.logspace(-3 ,1 ,10 ,math.pi/2)
    Temp2 = np.append(
        Temp,
        np.linspace(1.5802 ,math.pi ,uppersurface_panel)
      )
    #print(np.linspace(1.5802 ,math.pi ,uppersurface_panel))
    #print(Temp2)
    new_uppersurfaceX = np.zeros(Temp2.size)
    for i in range(Temp2.size):
        new_uppersurfaceX[i] = -(-0.5  + 0.5 * math.cos(Temp2[i]))
    print("Temp ",Temp2[i])
    new_uppersurfaceX = np.delete(new_uppersurfaceX ,0)
    for i in range(Temp2.size):
        print(new_uppersurfaceX[i])


    new_uppersurfaceY = uppersurface_interpolate_function(new_uppersurfaceX)

    new_dataX = np.concatenate([new_lowersurfaceX, new_uppersurfaceX[1:]])
    new_dataY = np.concatenate([new_lowersurfaceY, new_uppersurfaceY[1:]])
    new_data = list(zip(new_dataX, new_dataY))

    return new_data
