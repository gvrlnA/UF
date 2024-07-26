#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sympy import *
import math as mp
import openpyxl
import statistics
from scipy.optimize import curve_fit

def mapping(values_x, a_mapping, b_mapping, c_mapping, d_mapping): 
    return a_mapping * values_x**3 + b_mapping * values_x**2 + c_mapping * values_x + d_mapping

def abscissa_graduation(z):
    return np.linspace(z[0], z[len(z) - 1], round((z[len(z) - 1] - z[0])*1000))

# function to check string
def check(s, arr):
    # returns a list of booleans
    result = [characters in s for characters in arr]
    return result

def spline_force(abscissa, ordinate, degree):
    sz = symbols('z')
    spl_ordinate = interpolating_spline(degree,sz,abscissa,ordinate)
    spline_ordinate = []
    for point in abscissa_graduation(abscissa):
        spline_ordinate.append(spl_ordinate.subs(sz, point))
    return spline_ordinate, spl_ordinate

def uni_delta_z_func(z_elem, hy_elem, file_name, sheet_name, z_inf, z_sup):
    spline_ordinate, pressure_distribution = spline_force(z_elem, hy_elem, 1) #строим сплайн по размаху

    #оставляем только положительную часть давления
    pressure = []
    pressure_cord = []
    z_graduation = abscissa_graduation(z_elem)
    for i in range(len(spline_ordinate)):
        if ((spline_ordinate[i]>=0) and (z_inf<=z_graduation[i]<=z_sup)):
            pressure.append(spline_ordinate[i]) 
            pressure_cord.append(z_graduation[i])

    straps_cord = pd.read_excel(file_name, sheet_name=sheet_name, index_col=0)

    z_centre = list(straps_cord.loc['Координаты по Z:'])
    z_centre = [z_centre[i]/1000 for i in range(len(z_centre))]

    plt.figure(figsize=(10,10))
    plt.plot(pressure_cord, pressure)
    plt.scatter(z_centre, [0 for i in range(len(z_centre))])
    plt.xlabel("z")
    plt.ylabel("Hy")
    plt.grid()
    plt.show()

    arr = ['I']

    right_results = []
    sz = symbols('z')
    a = pressure[0] #первый столбец давления
    z_start = pressure_cord[0] #координата первого столбца давления
    for j in range(len(z_centre)-1):
        group_of_results = []
        difference = []
        for i in range(len(pressure_distribution.args)): 
            equation = (pressure_distribution.args[i][0].subs(sz, z_start+sz))*(sz-3*(z_centre[j]-z_start))+2*a*sz-3*(z_centre[j]-z_start)*a 
            result = solve(equation, sz)
            for n in range(len(result)):
                if (((any(check(str(result[n]), arr))) != True) and (result[n]>0)):
                    if ((z_start+result[n]>z_centre[j]) and (z_start+result[n]<z_centre[j+1])):
                        group_of_results.append(result[n])
                        difference.append(abs(statistics.mean([z_centre[j], z_centre[j+1]])-z_start-result[n]))
        if (len(group_of_results)!=0):
            right_results.append(group_of_results[difference.index(min(difference))])
        print('right_result ', j, ' : ', right_results[len(right_results)-1])
        a = pressure_distribution.args[i][0].subs(sz, z_start+right_results[len(right_results)-1])
        z_start += right_results[len(right_results)-1]

    z_start = pressure_cord[0]
    plt.figure(figsize=(10,10))
    plt.plot(pressure_cord, pressure)
    plt.scatter(z_centre, [0 for i in range(len(z_centre))])
    for i in range(len(right_results)):
        plt.scatter(z_start + right_results[i], 0, color='red')
        z_start = z_start + right_results[i]
    plt.xlabel("z")
    plt.ylabel("Hy")
    plt.grid()

    delta_z_elem = right_results.copy()
    delta_z_elem.append(z_elem[len(z_elem)-1]-sum(right_results)-pressure_cord[0])
    return delta_z_elem


# In[ ]:




