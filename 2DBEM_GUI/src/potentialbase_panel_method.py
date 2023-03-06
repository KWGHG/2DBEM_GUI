from ast import main
import numpy as np
import math
import CT2D

def BEM(inletvelocity ,inletangle ,geometry):
    velocity = np.zeros(2)
    velocity[0] = inletvelocity * math.cos(inletangle * math.pi / 180)
    velocity[1] = inletvelocity * math.sin(inletangle * math.pi / 180)
    #定義尾跡流
    Wake = np.zeros(2)
    Wake[0] = geometry[0,0] + 1000 * math.cos(inletangle * math.pi / 180 )
    Wake[1] = geometry[0,1] + 1000 * math.sin(inletangle * math.pi / 180)

    #建立矩陣
    collocation = np.zeros([geometry.shape[0] - 1 ,2])
    theta = np.zeros(geometry.shape[0] - 1)
    normal_vector = np.zeros([geometry.shape[0] - 1 ,2])
    collocation_panel_length = np.zeros(geometry.shape[0] - 2)
    panel_length = np.zeros(geometry.shape[0] - 1 )

    #建立Collocation matrix
    for i in range(geometry.shape[0] - 1):
        collocation[i,0] = 0.5 * (geometry[i+1 ,0] - geometry[i ,0]) + geometry[i,0]
        collocation[i,1] = 0.5 * (geometry[i+1 ,1] - geometry[i ,1]) + geometry[i,1]
        dx = geometry[i + 1, 0] - geometry[i, 0]
        dy = geometry[i + 1, 1] - geometry[i, 1]
        panel_length[i] = math.sqrt(pow(dx ,2) + pow(dy ,2))
        theta[i] = math.atan2(dy ,dx)
    
    for i in range(geometry.shape[0] - 2):
        dx = collocation[i+1 ,0] - collocation[i ,0]
        dy = collocation[i+1 ,1] - collocation[i ,1]
        collocation_panel_length[i] = math.sqrt(pow(dx ,2) + pow(dy ,2))

    #計算誘導函數
    A_Matrix = np.zeros([geometry.shape[0] - 1 ,geometry.shape[0] - 1])
    B1_Matrix = np.zeros([geometry.shape[0] - 1 ,geometry.shape[0] - 1])
    B_Matrix = np.zeros([geometry.shape[0] - 1 ,1])
    C_Matrix = np.zeros([geometry.shape[0] - 1 ,1])

    for i in range(geometry.shape[0] - 1):
        for j in range(geometry.shape[0] - 1):
            if i == j:
                A_Matrix[i, j] = 0.5
                B1_Matrix[i, j] = strengh_of_source(collocation[i, 0], collocation[i, 1], geometry[j, 0], geometry[j, 1]            
					, geometry[j + 1, 0], geometry[j + 1, 1], 2)
                C_Matrix[i, 0] = velocity[0] * math.sin(theta[i]) + velocity[1] * -math.cos(theta[i])
            else:
                var1 = strengh_of_doublet(collocation[i, 0], collocation[i, 1], geometry[j, 0], geometry[j, 1]
					, geometry[j + 1, 0], geometry[j + 1, 1], 1)
                var2 = strengh_of_source(collocation[i, 0], collocation[i, 1], geometry[j, 0], geometry[j, 1]
					, geometry[j + 1, 0], geometry[j + 1, 1], 1)
                A_Matrix[i, j] = var1
                B1_Matrix[i, j] = var2  
    
    for i in range(geometry.shape[0] - 1):
        wake_coefficient = strengh_of_doublet(collocation[i, 0], collocation[i, 1], geometry[0, 0]
			, geometry[0, 1], Wake[0], Wake[1], 2)
        Temp = A_Matrix[i, 0]
        A_Matrix[i, 0] = Temp - wake_coefficient
        Temp = A_Matrix[i, -1]
        A_Matrix[i, -1] = Temp + wake_coefficient

    #解線性矩陣
    B_Matrix = B1_Matrix.dot(C_Matrix)
   
    Ans =  np.linalg.solve(A_Matrix,B_Matrix)
    VelocityT = np.zeros( geometry.shape[0])
    CP = np.zeros([geometry.shape[0] ,2])
    PHI = np.zeros(geometry.shape[0]-1)
    Force = np.zeros(2)
    for i in range(geometry.shape[0]-1):
        PHI[i] = collocation[i, 0] * math.cos(inletangle * math.pi / 180) + collocation[i, 1] \
                    * math.sin(inletangle * math.pi / 180) + Ans[i][0] 
    VelocityT[0] = 0
    VelocityT[-1] = 0
    CP[0,0] = geometry[0, 0]
    CP[0, 1] = 1
    CP[-1, 0] = geometry[-1, 0]
    CP[-1, 1] = 1
    CL = 0
    for i in range(geometry.shape[0]-2):
        VelocityT[i+1] = (PHI[i] - PHI[i + 1]) / collocation_panel_length[i]
         
        CP[i+1, 0] = geometry[i + 1, 0]
        CP[i+1, 1] = (1 - pow(VelocityT[i + 1], 2))
        if VelocityT[i + 1] > 0.0001 or VelocityT[i + 1] < -0.001 :
            Force[0] += CP[i+1, 1] * panel_length[i + 1] * math.sin(theta[i + 1])
            Force[1] += CP[i+1, 1] * panel_length[i + 1] * -math.cos(theta[i+1])
    

    for i in range(geometry.shape[0]-2):
        CP[i, 1] = -CP[i, 1]

    CL = -Force[0] * math.sin(inletangle * math.pi / 180) + Force[1] * math.cos(inletangle * math.pi / 180)
    return CL ,CP

def strengh_of_doublet(xi ,yi ,xj1 ,yj1 ,xj2 ,yj2 ,index):
    theta = math.atan2(yj2 - yj1, xj2 - xj1)
    XP = np.zeros(2)
    X1 = np.zeros(2)
    X2 = np.zeros(2)    
    XPt = np.zeros(2)
    X1t = np.zeros(2)
    X2t = np.zeros(2)    
    XP[0] = xi
    XP[1] = yi
    X1[0] = xj1
    X1[1] = yj1
    X2[0] = xj2
    X2[1] = yj2
    X2t = CT2D.rotating(CT2D.translation(X2 ,-X1[0] ,-X1[1]) ,-theta)
    XPt = CT2D.rotating(CT2D.translation(XP ,-X1[0] ,-X1[1]) ,-theta)

    if index == 1:
        angle1 = math.atan2(XPt[1] ,XPt[0] - X2t[0])
        angle2 = math.atan2(XPt[1] , XPt[0])
        a1 = -0.1591549431 * (angle1 - angle2)
    else:
        angle1 = math.atan(XPt[1] / (XPt[0] - X2t[0]))
        angle2 = math.atan(XPt[1] / XPt[0])
        a1 = -0.1591549431 * (angle1 - angle2)

    return a1

def strengh_of_source(xi ,yi ,xj1 ,yj1 ,xj2 ,yj2 ,index):
    theta = math.atan2(yj2 - yj1, xj2 - xj1)
    XP = np.zeros(2)
    X1 = np.zeros(2)
    X2 = np.zeros(2)    
    XPt = np.zeros(2)
    X1t = np.zeros(2)
    X2t = np.zeros(2)    
    XP[0] = xi
    XP[1] = yi
    X1[0] = xj1
    X1[1] = yj1
    X2[0] = xj2
    X2[1] = yj2
    
    X2t = CT2D.rotating(CT2D.translation(X2 ,-X1[0] ,-X1[1]) ,-theta)
    XPt = CT2D.rotating(CT2D.translation(XP ,-X1[0] ,-X1[1]) ,-theta)
    R1 = pow(XPt[0], 2) + pow(XPt[1], 2)
    R2 = pow(XPt[0] - X2t[0], 2) + pow(XPt[1], 2)
    angle1 = math.atan2(XPt[1], XPt[0] - X2t[0])
    angle2 = math.atan2(XPt[1], XPt[0])
    
    if index == 1:
        a1 = 0.07957747155 * (XPt[0] * math.log(R1) - (XPt[0] - X2t[0]) * math.log(R2) + 2 * XPt[1] 
                              * (angle1 - angle2))
    else:
        a1 = 0.1591549431 * XPt[0] * math.log(R1)

    return a1

#if __name__ == "__main__":
#    row = 0
#    file = open("naca0012.dat")
#    lines = file.readlines()
#    for line in lines:
#        row += 1
#    file.close()

#    file = open("naca0012.dat")
#    data = np.empty((row, 2))
#    lines = file.readlines()
#    row = 0
#    for line in lines:
#        list1 = line.strip().split()
#        data[row, :] = list1[:]
#        row += 1
#    BEM(1,5,data)
#    file.close()
