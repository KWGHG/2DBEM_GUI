import numpy as np
from scipy import interpolate


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
    for line in lines:
        list1 = line.strip().split()
        data[row, :] = list1[:]
        row += 1
    file.close()
    index = (row + 1) / 2
    lowersurfaceX = np.flip(data[0 : int(index), 0])
    lowersurfaceY = np.flip(data[0 : int(index), 1])
    uppersurfaceX = data[int(index - 1) : int(row), 0]
    uppersurfaceY = data[int(index - 1) : int(row), 1]
    lowersurface_interpolate_function = interpolate.CubicSpline(
        lowersurfaceX, lowersurfaceY
    )
    uppersurface_interpolate_function = interpolate.CubicSpline(
        uppersurfaceX, uppersurfaceY
    )
    if (numbers_of_panel % 2) == 0:
        lowersurface_panel = int(numbers_of_panel / 2 + 1)
        uppersurface_panel = int(numbers_of_panel / 2 + 1)
    else:
        lowersurface_panel = int(numbers_of_panel / 2 + 2)
        uppersurface_panel = int(numbers_of_panel / 2 + 1)
    

    Temp = np.append(
        np.linspace(1 ,0.9 ,int(lowersurface_panel * 0.2)),
        np.linspace(0.8999999 ,0.200001 ,int(lowersurface_panel * 0.2)),
    )

    new_lowersurfaceX = np.append(
        Temp,
        np.logspace(1 ,7 ,int(lowersurface_panel * 0.6) ,base=0.2),
    )
    new_lowersurfaceY = lowersurface_interpolate_function(new_lowersurfaceX)

    Temp = np.append(
        np.logspace(7, 1, int(uppersurface_panel * 0.6) ,base=0.2),
        np.linspace(0.200001, 0.9, int(uppersurface_panel * 0.2)),
    )

    new_uppersurfaceX = np.append(
        Temp,
        np.linspace(0.900001, 1, int(uppersurface_panel * 0.2))
    )
    new_uppersurfaceY = uppersurface_interpolate_function(new_uppersurfaceX)
    new_dataX = np.concatenate([new_lowersurfaceX, new_uppersurfaceX[1:]])
    new_dataY = np.concatenate([new_lowersurfaceY, new_uppersurfaceY[1:]])
    new_data = list(zip(new_dataX, new_dataY))

    return new_data
