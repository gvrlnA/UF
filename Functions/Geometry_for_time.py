#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sympy import *
import math as mp
import statistics
from scipy.optimize import curve_fit


# In[11]:


# elem&var&dep should be object type 
def geometry(elem, var, dep):
    pds_geom=pd.read_excel('геометрия.xlsx',sheet_name=elem)
    list_name=pds_geom.columns.tolist()
    array_points=[]
    for i in range(len(list_name)):
        g=[]
        g=list(pds_geom[list_name[i]].dropna())
        if len(g) != 0:
            for j in range(len(g)):
                array_points.append(g[j])

    points=[]
    for i in range(len(array_points)):
        points.append(array_points[i].split(';'))

    Front_line=[]
    Back_line=[]
    for i in range(len(points)):
        if points[i][3] == 'front':
            Front_line.append(points[i])
        else:
            Back_line.append(points[i])
    Front_line.sort(key=lambda x: x[4])
    Back_line.sort(key=lambda x: x[4])
    
    for i in Front_line:
        for j in range(len(i)):
            if j < 3:
                i[j] = float(i[j]) 
            
    for i in Back_line:
        for j in range(len(i)):
            if j < 3:
                i[j] = float(i[j])

    if var == 'x':
        s = symbols('x')
        if dep == 'x':
            print('error dependencies')
            
        elif dep =='y':
            if len(Front_line) == 2:
                if round(Front_line[1][1]) == round(Front_line[0][1]):
                    Front = Piecewise((Front_line[1][1], (s >= Front_line[0][0]) & (s <= Front_line[1][0])))
                else:
                    m = (Front_line[1][1] - Front_line[0][1]) / (Front_line[1][0] - Front_line[0][0])
                    line_eq = m * (s - Front_line[0][0]) + Front_line[0][1]
                    Front = Piecewise((line_eq, (s >= Front_line[0][0]) & (s <= Front_line[1][0])))
            if len(Back_line) == 2:
                if round(Back_line[1][1]) == round(Back_line[0][1]):
                    Back = Piecewise((Back_line[1][1], (s >= Back_line[0][0]) & (s <= Back_line[1][0])))
                else:
                    m = (Back_line[1][1] - Back_line[0][1]) / (Back_line[1][0] - Back_line[0][0])
                    line_eq = m * (s - Back_line[0][0]) + Back_line[0][1]
                    Back = Piecewise((line_eq, (s >= Back_line[0][0]) & (s <= Back_line[1][0])))
            if len(Front_line) > 2:
                Front=interpolating_spline(1, s, [float(Front_line[i][0]) for i in range(len(Front_line))], [float(Front_line[i][1]) for i in range(len(Front_line))])
            if len(Back_line) > 2:
                Back=interpolating_spline(1, s, [float(Back_line[i][0]) for i in range(len(Back_line))], [float(Back_line[i][1]) for i in range(len(Back_line))])
            
        else:
            if len(Front_line) == 2:
                if round(Front_line[1][2]) == round(Front_line[0][2]):
                    Front = Piecewise((Front_line[1][2], (s >= Front_line[0][0]) & (s <= Front_line[1][0])))
                else:
                    m = (Front_line[1][2] - Front_line[0][2]) / (Front_line[1][0] - Front_line[0][0])
                    line_eq = m * (s - Front_line[0][0]) + Front_line[0][2]
                    Front = Piecewise((line_eq, (s >= Front_line[0][0]) & (s <= Front_line[1][0])))
            if len(Back_line) == 2:
                if round(Back_line[1][2]) == round(Back_line[0][2]):
                    Back = Piecewise((Back_line[1][2], (s >= Back_line[0][0]) & (s <= Back_line[1][0])))
                else:
                    m = (Back_line[1][2] - Back_line[0][2]) / (Back_line[1][0] - Back_line[0][0])
                    line_eq = m * (s - Back_line[0][0]) + Back_line[0][2]
                    Back = Piecewise((line_eq, (s >= Back_line[0][0]) & (s <= Back_line[1][0])))
            if len(Front_line) > 2:
                Front=interpolating_spline(1, s, [float(Front_line[i][0]) for i in range(len(Front_line))], [float(Front_line[i][2]) for i in range(len(Front_line))])
            if len(Back_line) > 2:
                Back=interpolating_spline(1, s, [float(Back_line[i][0]) for i in range(len(Back_line))], [float(Back_line[i][2]) for i in range(len(Back_line))])
                 
    elif var == 'y':
        s = symbols('y')
        if dep == 'x':
            if len(Front_line) == 2:
                if round(Front_line[1][0]) == round(Front_line[0][0]):
                    Front = Piecewise((Front_line[1][0], (s >= Front_line[0][1]) & (s <= Front_line[1][1])))
                else:
                    m = (Front_line[1][0] - Front_line[0][0]) / (Front_line[1][1] - Front_line[0][1])
                    line_eq = m * (s - Front_line[0][1]) + Front_line[0][0]
                    Front = Piecewise((line_eq, (s >= Front_line[0][1]) & (s <= Front_line[1][1])))
            if len(Back_line) == 2:
                if round(Back_line[1][0]) == round(Back_line[0][0]):
                    Back = Piecewise((Back_line[1][0], (s >= Back_line[0][1]) & (s <= Back_line[1][1])))
                else:
                    m = (Back_line[1][0] - Back_line[0][0]) / (Back_line[1][1] - Back_line[0][1])
                    line_eq = m * (s - Back_line[0][1]) + Back_line[0][0]
                    Back = Piecewise((line_eq, (s >= Back_line[0][1]) & (s <= Back_line[1][1])))
            if len(Front_line) > 2:
                Front=interpolating_spline(1, s, [float(Front_line[i][1]) for i in range(len(Front_line))], [float(Front_line[i][0]) for i in range(len(Front_line))])
            if len(Back_line) > 2:
                Back=interpolating_spline(1, s, [float(Back_line[i][1]) for i in range(len(Back_line))], [float(Back_line[i][0]) for i in range(len(Back_line))])
            
        elif dep =='y':
            print('error dependencies')
            
        else:
            if len(Front_line) == 2:
                if round(Front_line[1][2]) == round(Front_line[0][2]):
                    Front = Piecewise((Front_line[1][2], (s >= Front_line[0][1]) & (s <= Front_line[1][1])))
                else:
                    m = (Front_line[1][2] - Front_line[0][2]) / (Front_line[1][1] - Front_line[0][1])
                    line_eq = m * (s - Front_line[0][1]) + Front_line[0][2]
                    Front = Piecewise((line_eq, (s >= Front_line[0][1]) & (s <= Front_line[1][1])))
            if len(Back_line) == 2:
                if round(Back_line[1][2]) == round(Back_line[0][2]):
                    Back = Piecewise((Back_line[1][2], (s >= Back_line[0][1]) & (s <= Back_line[1][1])))
                else:
                    m = (Back_line[1][2] - Back_line[0][2]) / (Back_line[1][1] - Back_line[0][1])
                    line_eq = m * (s - Back_line[0][1]) + Back_line[0][2]
                    Back = Piecewise((line_eq, (s >= Back_line[0][1]) & (s <= Back_line[1][1])))
            if len(Front_line) > 2:
                Front=interpolating_spline(1, s, [float(Front_line[i][1]) for i in range(len(Front_line))], [float(Front_line[i][2]) for i in range(len(Front_line))])
            if len(Back_line) > 2:
                Back=interpolating_spline(1, s, [float(Back_line[i][1]) for i in range(len(Back_line))], [float(Back_line[i][2]) for i in range(len(Back_line))])
        
    else:
        s = symbols('z')
        if dep == 'x':
            if len(Front_line) == 2:
                if round(Front_line[1][0]) == round(Front_line[0][0]):
                    Front = Piecewise((Front_line[1][0], (s >= Front_line[0][2]) & (s <= Front_line[1][2])))
                else:
                    m = (Front_line[1][0] - Front_line[0][0]) / (Front_line[1][2] - Front_line[0][2])
                    line_eq = m * (s - Front_line[0][2]) + Front_line[0][0]
                    Front = Piecewise((line_eq, (s >= Front_line[0][2]) & (s <= Front_line[1][2])))
            if len(Back_line) == 2:
                if round(Back_line[1][0]) == round(Back_line[0][0]):
                    Back = Piecewise((Back_line[1][0], (s >= Back_line[0][2]) & (s <= Back_line[1][2])))
                else:
                    m = (Back_line[1][0] - Back_line[0][0]) / (Back_line[1][2] - Back_line[0][2])
                    line_eq = m * (s - Back_line[0][2]) + Back_line[0][0]
                    Back = Piecewise((line_eq, (s >= Back_line[0][2]) & (s <= Back_line[1][2])))
            if len(Front_line) > 2:
                Front=interpolating_spline(1, s, [float(Front_line[i][2]) for i in range(len(Front_line))], [float(Front_line[i][0]) for i in range(len(Front_line))])
            if len(Back_line) > 2:
                Back=interpolating_spline(1, s, [float(Back_line[i][2]) for i in range(len(Back_line))], [float(Back_line[i][0]) for i in range(len(Back_line))])
            
        elif dep =='y':
            if len(Front_line) == 2:
                if round(Front_line[1][1]) == round(Front_line[0][1]):
                    Front = Piecewise((Front_line[1][1], (s >= Front_line[0][2]) & (s <= Front_line[1][2])))
                else:
                    m = (Front_line[1][1] - Front_line[0][1]) / (Front_line[1][2] - Front_line[0][2])
                    line_eq = m * (s - Front_line[0][2]) + Front_line[0][1]
                    Front = Piecewise((line_eq, (s >= Front_line[0][2]) & (s <= Front_line[1][2])))
            if len(Back_line) == 2:
                if round(Back_line[1][1]) == round(Back_line[0][1]):
                    Back = Piecewise((Back_line[1][1], (s >= Back_line[0][2]) & (s <= Back_line[1][2])))
                else:
                    m = (Back_line[1][1] - Back_line[0][1]) / (Back_line[1][2] - Back_line[0][2])
                    line_eq = m * (s - Back_line[0][2]) + Back_line[0][1]
                    Back = Piecewise((line_eq, (s >= Back_line[0][2]) & (s <= Back_line[1][2])))
            if len(Front_line) > 2:
                Front=interpolating_spline(1, s, [float(Front_line[i][2]) for i in range(len(Front_line))], [float(Front_line[i][1]) for i in range(len(Front_line))])
            if len(Back_line) > 2:
                Back=interpolating_spline(1, s, [float(Back_line[i][2]) for i in range(len(Back_line))], [float(Back_line[i][1]) for i in range(len(Back_line))])
            
        else:
            print('error dependencies')
    return Front, Back, Front_line, Back_line

def boundary_points(Front_line, Back_line, var):
    var_lst = ['x', 'y', 'z']
    for i in range(len(var_lst)):
        if var == var_lst[i]:
            start_ord = Front_line[0][i]
            finish_ord = Front_line[len(Front_line)-1][i]
    return start_ord, finish_ord

