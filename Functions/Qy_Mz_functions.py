#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sympy import *
import math as mp
import openpyxl


# In[2]:
sx = symbols('x')
sz = symbols('z')

def Finding_sechenie(list_name, sechenie_list):
    out_list=[]
    for i in range(len(list_name)):
        find=list_name[i].split('=')
        for j in range(len(sechenie_list)):
            if find[-1] == sechenie_list[j]:
                out_list.append(list_name[i])
            else: 
                continue
    return out_list


# In[3]:


def grad_Force_along_horde(data_base, sechenie_list, deltas):
    list_name=data_base.columns.tolist()
    list_name_for_one_element=[]
    for i in range(len(list_name)):
        find=list_name[i].split('=')
        for j in range(len(sechenie_list)):
            if find[-1] == sechenie_list[j]:
                list_name_for_one_element.append(list_name[i])
            else: 
                continue
    b=[v for k,v in enumerate(list_name_for_one_element) if not k%2]
    c=[v for k,v in enumerate(list_name_for_one_element) if k%2]
    splines_hy=[]
    x_secheniy=[]
    for i in range(len(c)):
        xnp=[[data_base[b[i]][j],data_base[c[i]][j]] for j in range(len(data_base[b[0]])-1)]
        xnp_wo_nan=[]
        for p in range(len(xnp)):
            if not mp.isnan(xnp[p][1]):
                xnp_wo_nan.append(xnp[p])
        x_wo_nan=[xnp_wo_nan[i][0] for i in range(len(xnp_wo_nan))]
        p_wo_nan=[xnp_wo_nan[i][1] for i in range(len(xnp_wo_nan))]
        spl_up=interpolating_spline(2,sx, x_wo_nan[:len(x_wo_nan)//2], p_wo_nan[:len(p_wo_nan)//2])
        spl_down=interpolating_spline(2,sx,x_wo_nan[len(x_wo_nan)//2:], p_wo_nan[len(p_wo_nan)//2:])
        spl_p=spl_down-spl_up
        spl_hy_x=spl_p*deltas[i]
        splines_hy.append(spl_hy_x)
        x_secheniy.append(x_wo_nan)
    sechenia=[]
    for i in range(len(c)):
        peremennaya=c[i].split('=')[-1]
        muhammed_ebaniy = float(peremennaya.replace(',', '.'))
        sechenia.append(muhammed_ebaniy)
    grad_f=[[splines_hy[i],x_secheniy[i][:len(x_secheniy[i])//2],sechenia[i]] for i in range(len(c))]
    return grad_f


# In[4]:



def Forces(grad_arr, geometry, ax_str):
    b=interpolating_spline(1, sx, geometry[1], geometry[0])
    Qy=[]
    for i in range(len(grad_arr)):
        Qy.append(integrate(grad_arr[i][0], (sx,grad_arr[i][1][len(grad_arr[i][1])-1]-b.subs(sx,grad_arr[i][2]), grad_arr[i][1][len(grad_arr[i][1])-1])))
    x_arr=[grad_arr[i][1] for i in range(len(grad_arr))]
    hy_arr=[[grad_arr[i][0].subs(sx, x_arr[i][j]) for j in range(len(x_arr[i]))]for i in range(len(grad_arr)) ]
    x_otnstr=[]
    for i in range(len(x_arr)):
        coord_str=ax_str.subs(sz, grad_arr[i][2])
        massive_cringa=[]
        for j in range(len(x_arr[i])):
            massive_cringa.append(x_arr[i][j]-coord_str)
        x_otnstr.append(massive_cringa)
    Mz=[]
    for i in range(len(x_otnstr)):
        spl_hy_str=interpolating_spline(2, sx, x_otnstr[i], hy_arr[i])
        dMz=spl_hy_str*sx
        Mz_sech=integrate(dMz,(sx,x_otnstr[i][len(x_otnstr[i])-1]-b.subs(sx,grad_arr[i][2]), x_otnstr[i][len(x_otnstr[i])-1]))
        Mz.append(Mz_sech)
    
    return Qy, Mz


# In[ ]:




