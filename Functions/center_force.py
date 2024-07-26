#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import LeverSystemForce_Library as lsfl
from scipy.integrate import simps
from sympy import *
from sympy import symbols
import pandas as pd


# In[2]:

sx = symbols('x')


def center_from_mass_dist(dist_cm_element_ord, dist_cm_element_absc, dist_cm_element_m, xl_element):
    cm_ord, cm_absc, cm_m = [], [], []
    for i in range(len(dist_cm_element_ord)):
        for j in range(len(xl_element)):
            if round(dist_cm_element_ord[i], 3)==round(float(xl_element[j]), 3):
                cm_ord.append(dist_cm_element_ord[i])
                cm_absc.append(dist_cm_element_absc[i])
                cm_m.append(dist_cm_element_m[i])
    return cm_ord, cm_absc, cm_m


# In[3]:


def center_force_func(grad_F):

    center_of_force = []

    for i in range(len(grad_F)): 

        # Загрузка данных из криволинейного графика приложения силы (x - координата, y - значение силы)
        x = lsfl.abscissa_graduation([grad_F[i][1][0], grad_F[i][1][len(grad_F[i][1])-1]])
        y = []
        for point in x:
            y.append(grad_F[i][0].subs(sx, point))
        y = np.array(y)

        # Вычисление момента силы
        moment = simps(y * x, x)

        # Вычисление суммарной силы
        total_force = simps(y, x)

        # Нахождение положения центра масс
        center_of_force.append(moment / total_force)

        print("Положение центра приложения сил:", center_of_force[len(center_of_force)-1])
    return center_of_force


# In[4]:


def sum_Qy(cm_m, Qy):
    sum_Qy = (-1)*np.array(cm_m) + np.array(Qy)
    return sum_Qy


# In[5]:

def sum_Mz(Mz, center_of_force, cm_m, name_of_element):
    sz=symbols('z')
    PK=[0.824, 0.0, 0.0, 0.0, 0.0, 0.824]
    z_PK=[-8.27, -4.558, -0.78, 0.78, 4.558, 8.27]
    BK=[1.824, 2.0, 2.0, 2.0, 2.0, 1.824]
    z_BK=[-8.27, -5.27, -0.78, 0.78, 5.27, 8.27]
    spl_PK=interpolating_spline(1, sz, z_PK, PK)
    spl_BK=interpolating_spline(1, sz, z_BK, BK)
    b_hor = interpolating_spline(1, sz, z_BK, BK)-interpolating_spline(1, sz, z_PK, PK)
    str_ax=0.275
    spl_str=spl_PK+str_ax*b_hor+1.88
    
    straps_cord = pd.read_excel('Координаты лямок.xlsx', sheet_name=name_of_element, index_col=0)
    z_center = list(straps_cord.loc['Координаты по Z:'])
    z_center = [z_center[i]/1000 for i in range(len(z_center))]
    str_ax_in_section = []
    for i in range(len(z_center)):
        str_ax_in_section.append(spl_str.subs(sz, z_center[i]))
    sum_Mz = np.array(Mz) + (np.array(center_of_force) - np.array(str_ax_in_section))*np.array(cm_m)*(-1) 
    return sum_Mz


# In[ ]:




