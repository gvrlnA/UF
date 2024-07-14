#!/usr/bin/env python
# coding: utf-8

# In[2]:


import scipy.optimize
from scipy.optimize import minimize
from scipy.optimize import Bounds
from scipy.optimize import LinearConstraint
import math
import numpy as np
from scipy.integrate import simps
from sympy import *
from sympy import symbols
import pandas as pd


# In[ ]:


def force_on_straps(sum_Qy, sum_Mz, name_of_element):
    
    sz=symbols('z')
    PK=[0.824, 0.0, 0.0, 0.0, 0.0, 0.824]
    z_PK=[-8.27, -4.558, -0.78, 0.78, 4.558, 8.27]
    BK=[1.824, 2.0, 2.0, 2.0, 2.0, 1.824]
    z_BK=[-8.27, -5.27, -0.78, 0.78,5.27,8.27]
    spl_PK=interpolating_spline(1, sz, z_PK, PK)
    spl_BK=interpolating_spline(1, sz, z_BK, BK)
    b_hor = interpolating_spline(1, sz, z_BK, BK)-interpolating_spline(1, sz, z_PK, PK)
    str_ax=0.275
    spl_str=spl_PK+str_ax*b_hor+1.88
    
    er = 0 #допустимая ошибка в долях
    
    def objective(x):
        return sum(abs(np.dot(A, x) - b))
    
    straps_cord = pd.read_excel('Координаты лямок.xlsx', sheet_name=name_of_element, index_col=0)
    z_center = list(straps_cord.loc['Координаты по Z:'])
    z_center = [z_center[i]/1000 for i in range(len(z_center))]
    for i in range(len(z_center)):
        print(i)
        straps_cord_x = straps_cord.iloc[1:, i].tolist()
        for j in range(len(straps_cord_x)-1, -1, -1):
            if str(straps_cord_x[j]) == 'nan':
                straps_cord_x.pop(j)
        if len(straps_cord_x)>=2:
            straps_cord_x = [_/1000 for _ in straps_cord_x]
            for j in range(len(straps_cord_x)):
                straps_cord_x[j] = float(straps_cord_x[j] + 1.88 - spl_str.subs(sz, z_center[i]))        
            #print(straps_cord_x) #отладка

            A = [
                    # Qy
                    [1 for j in range(len(straps_cord_x))],
                    # Mz
                    [straps_cord_x[j] for j in range(len(straps_cord_x))]
                ]

            b = [
                    # Qy
                    sum_Qy[i],
                    # Mz
                    sum_Mz[i]
                ]

            print(A)
            print(b)

            bounds = Bounds([10 for j in range(len(straps_cord_x))], [np.inf for j in range(len(straps_cord_x))])
            linear_constraint = LinearConstraint(A, [b[i]*(1 - er) for i in range(len(b))], [b[i]*(1 + er) for i in range(len(b))], keep_feasible=False)
            lsq = minimize(objective, np.zeros([len(straps_cord_x)]), method='trust-constr', constraints=[linear_constraint], hess=None, bounds=bounds)
            F = list(lsq.x)
            check = np.dot(A, F) - b
            print('Проверка: ', check)
            print('Погрешность %: ', [((np.dot(A[i], F)/b[i])-1)*100 for i in range(len(check))])
            print(F)
        else:
            continue
    return F, check

