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

def zakr_delta_z_func(z_zakr, hy_zakr):
    """Считаем delta_z на закрылок"""
    values_x = np.array(z_zakr)
    values_y = np.array(hy_zakr)

    args, _  = curve_fit(mapping, values_x, values_y) 

    spline_ordinate, pressure_distribution = mapping(abscissa_graduation(z_zakr), *args), args

    #оставляем только положительную часть давления
    pressure = []
    pressure_cord = []
    z_graduation = abscissa_graduation(z_zakr)
    for i in range(len(spline_ordinate)):
        if ((spline_ordinate[i]>=0) and (z_graduation[i]<=5.270)):
            pressure.append(spline_ordinate[i]) 
            pressure_cord.append(z_graduation[i])

    straps_cord = pd.read_excel('Координаты лямок.xlsx', sheet_name='Закрылок', index_col=0)

    z_centre = list(straps_cord.loc['Координаты по Z:'])
    z_centre = [z_centre[i]/1000 for i in range(len(z_centre))]

    plt.figure(figsize=(10,10))
    plt.plot(z_zakr, hy_zakr)
    plt.scatter(z_centre, [0 for i in range(len(z_centre))])
    plt.xlabel("z")
    plt.ylabel("Hy")
    plt.grid()
    plt.show()

    arr = ['I']
    right_results = []
    sz = symbols('z')
    z_start = statistics.mean([z_centre[0], z_centre[1]])
    a = mapping(z_start, *args)
    for j in range(1, len(z_centre)-1):
        group_of_results = []
        difference = []
        equation = (mapping(z_start+sz, *args))*(sz-3*(z_centre[j]-z_start))+2*a*sz-3*(z_centre[j]-z_start)*a 
        result = solve(equation, sz)
        for n in range(len(result)):
            if (((any(check(str(result[n]), arr))) != True) and (result[n]>0)):
                if ((z_start+result[n]>z_centre[j]) and (z_start+result[n]<z_centre[j+1])):
                    group_of_results.append(result[n])
                    difference.append(abs(statistics.mean([z_centre[j], z_centre[j+1]])-(z_start+result[n])))
        if (len(group_of_results)!=0):
            right_results.append(group_of_results[difference.index(min(difference))])
        print('right_result ', j, ' : ', right_results[len(right_results)-1])
        a = mapping(z_start+right_results[len(right_results)-1], *args)
        z_start += right_results[len(right_results)-1]

    z_start = statistics.mean([z_centre[0], z_centre[1]])
    plt.figure(figsize=(10,10))
    plt.plot(z_zakr, hy_zakr)
    plt.plot(abscissa_graduation(z_zakr), mapping(abscissa_graduation(z_zakr), *args))
    plt.scatter(z_centre, [0 for i in range(len(z_centre))])
    plt.scatter(z_start, 0, color='red')
    for i in range(len(right_results)):
        plt.scatter(z_start + right_results[i], 0, color='red')
        z_start = z_start + right_results[i]
    plt.xlabel("z")
    plt.ylabel("Hy")
    plt.grid()

    right_results.insert(0, z_centre[1]-statistics.mean([z_centre[0], z_centre[1]]))
    delta_z_zakr = right_results.copy()
    delta_z_zakr.append(5.27-sum(right_results)-pressure_cord[0])
    return delta_z_zakr

def eler_delta_z_func(z_eler, hy_eler):
    """Считаем delta_z на элерон"""

    spline_ordinate, pressure_distribution = spline_force(z_eler, hy_eler, 1) #строим сплайн по размаху

    #оставляем только положительную часть давления
    pressure = []
    pressure_cord = []
    z_graduation = abscissa_graduation(z_eler)
    for i in range(len(spline_ordinate)):
        if ((spline_ordinate[i]>=0) and (z_graduation[i]>=5.270)):
            pressure.append(spline_ordinate[i]) 
            pressure_cord.append(z_graduation[i])

    straps_cord = pd.read_excel('Координаты лямок.xlsx', sheet_name='Элерон', index_col=0)

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

    delta_z_eler = right_results.copy()
    delta_z_eler.append(z_eler[len(z_eler)-1]-sum(right_results)-pressure_cord[0])
    return delta_z_eler

def kes_delta_z_func(z_kes, hy_kes):
    """Считаем delta_z на кессон"""

    spline_ordinate, pressure_distribution = spline_force(z_kes, hy_kes, 1) #строим сплайн по размаху

    #оставляем только положительную часть давления
    pressure = []
    pressure_cord = []
    z_graduation = abscissa_graduation(z_kes)
    for i in range(len(spline_ordinate)):
        if spline_ordinate[i]>=0:
            pressure.append(spline_ordinate[i]) 
            pressure_cord.append(z_graduation[i])

    straps_cord = pd.read_excel('Координаты лямок.xlsx', sheet_name='Кессон', index_col=0)

    z_centre = list(straps_cord.loc['Координаты по Z:'])
    z_centre = [z_centre[i]/1000 for i in range(len(z_centre))]
    z_centre.insert(6, 3.185)

    plt.figure(figsize=(10,10))
    plt.plot(z_kes, hy_kes)
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
        for i in range(len(pressure_distribution.args)):  
            equation = (pressure_distribution.args[i][0].subs(sz, z_start+sz))*(sz-3*(z_centre[j]-z_start))+2*a*sz-3*(z_centre[j]-z_start)*a 
            result = solve(equation, sz)
            for n in range(len(result)):
                if (((any(check(str(result[n]), arr))) != True) and (result[n]>0)):
                    if ((z_start+result[n]>z_centre[j]) and (z_start+result[n]<z_centre[j+1])):
                        group_of_results.append(result[n])
        if (len(group_of_results)!=0):
            right_results.append(min(group_of_results))
        print('right_result ', j, ' : ', right_results[len(right_results)-1])
        a = pressure_distribution.args[i][0].subs(sz, z_start+right_results[len(right_results)-1])
        z_start += right_results[len(right_results)-1]

    delta_z_kes = right_results.copy()
    delta_z_kes.append(z_kes[len(z_kes)-1]-sum(right_results)-pressure_cord[0])

    z_start = pressure_cord[0]
    plt.figure(figsize=(10,10))
    plt.plot(z_kes, hy_kes)
    plt.scatter(z_centre, [0 for i in range(len(z_centre))])
    for i in range(len(right_results)):
        plt.scatter(z_start + right_results[i], 0, color='red')
        z_start = z_start + right_results[i]
    plt.xlabel("z")
    plt.ylabel("Hy")
    plt.grid()
    plt.show()
    
    delta_z_kes[6] = delta_z_kes[6] + delta_z_kes[7]/2
    delta_z_kes[8] = delta_z_kes[8] + delta_z_kes[7]/2
    delta_z_kes.pop(7)
    return delta_z_kes

def uni_delta_z_func(z_elem, hy_elem, file_name, sheet_name, z_inf, z_sup):
    """Считаем delta_z на закрылок"""
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




