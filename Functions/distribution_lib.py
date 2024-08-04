#!/usr/bin/env python
# coding: utf-8

# In[3]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sympy import *
import math as mp

sx = symbols('x')

def general_dist():
    x_pk_abs=1.875
    pds_p=pd.read_excel('распределение Аштрих для distribution_lib.xlsx',index_col=0)

    z=[]
    p=pds_p['height'].fillna(0)
    for i in range(len(pds_p['height'])):
        if p[i+1] != 0:
            z.append(i)

    list_name=pds_p.columns.tolist()
    b=[v for k,v in enumerate(list_name) if not k%2]
    c=[v for k,v in enumerate(list_name) if k%2]

    #for i in range(len(c)-1):
    #    plt.plot(pds_p[c[i+1]][:z[1]], pds_p[b[i+2]][:z[1]])
    #    plt.plot(pds_p[c[i+1]][z[1]:], pds_p[b[i+2]][z[1]:])
    #plt.grid()
    #plt.xlabel("x")
    #plt.ylabel("p")
    #plt.show()

    hy=[]
    spl_up, spl_down = [], []
    for i in range(len(c)-1):
        spl_up.append(interpolating_spline(1,sx, pds_p[c[i+1]][:z[1]], pds_p[b[i+2]][:z[1]]))
        spl_down.append(interpolating_spline(1,sx,pds_p[c[i+1]][z[1]:], pds_p[b[i+2]][z[1]:]))
        spl_p=spl_down[i]-spl_up[i]
        hy.append(integrate(spl_p, (sx, pds_p[c[i+1]][:z[1]][1], pds_p[c[i+1]][:z[1]][len(pds_p[c[i+1]][:z[1]])])))
    hy.insert(0,hy[0])

    z_w=[0.78, 0.965, 1.533, 2.165, 2.761, 3.522, 4.326, 4.953, 5.672, 6.415, 7.135, 7.702, 8.081, 8.27]
    hy.append(0)
    return z_w, b, c, hy, pds_p, z, hy

def zakr_dist(z_w, b, c, pds_p, z):
    len_zakr=4.515
    width_zakr=0.743
    z_zakr=[0.78]
    for i in range(len(z_w)):
        if z_w[i] < len_zakr+0.78:
            z_zakr.append(z_w[i+1])
    print(z_zakr)

    hy_zakr=[]
    spl_down, spl_up = [], []
    for i in range(len(z_zakr)-1):
        spl_up.append(interpolating_spline(1,sx, pds_p[c[i+1]][:z[1]], pds_p[b[i+2]][:z[1]]))
        spl_down.append(interpolating_spline(1,sx,pds_p[c[i+1]][z[1]:], pds_p[b[i+2]][z[1]:]))
        spl_p=spl_down[i]-spl_up[i]
        hy_zakr.append(integrate(spl_p, (sx, pds_p[c[i+1]][:z[1]][len(pds_p[c[i+1]][:z[1]])]-width_zakr, pds_p[c[i+1]][:z[1]][len(pds_p[c[i+1]][:z[1]])])))
    hy_zakr.insert(0,hy_zakr[0])

    plt.plot(z_zakr, hy_zakr)
    plt.ylim(0, 340)
    plt.xlabel("z")
    plt.ylabel("Hy")
    plt.grid()
    plt.show()
    return z_zakr, hy_zakr

def eler_dist(z_w, b, c, pds_p, z):
    len_eler=2.974
    width1_eler=0.512
    widrth2_eler=0.294
    #eleron geometry
    points=[[width1_eler, width1_eler,widrth2_eler], [0.0, 8.27-len_eler, 8.27]]
    b_eler=interpolating_spline(1, sx, points[1], points[0])
    z_eler=[]
    for i in range(len(z_w)):
        if z_w[i] > 8.27-len_eler:
            z_eler.append(z_w[i-1])
    z_eler.append(8.27)
    print(z_eler)
    for i in range(len(z_eler)):
        print(b_eler.subs(sx, z_eler[i]))

    hy_eler=[]
    for i in range(len(z_eler)-1):
        spl_up=interpolating_spline(1,sx, pds_p[c[i+len(z_w)-len(z_eler)]][:z[1]], pds_p[b[i+1+len(z_w)-len(z_eler)]][:z[1]])
        spl_down=interpolating_spline(1,sx,pds_p[c[i+len(z_w)-len(z_eler)]][z[1]:], pds_p[b[i+1+len(z_w)-len(z_eler)]][z[1]:])
        spl_p=spl_down-spl_up
        hy_eler.append(integrate(spl_p, (sx, pds_p[c[i+len(z_w)-len(z_eler)]][:z[1]][len(pds_p[c[i+len(z_w)-len(z_eler)]][:z[1]])]-b_eler.subs(sx, z_eler[i]), pds_p[c[i+len(z_w)-len(z_eler)]][:z[1]][len(pds_p[c[i+len(z_w)-len(z_eler)]][:z[1]])])))
    hy_eler.append(0)

    plt.plot(z_eler, hy_eler)
    plt.ylim(0, 340)
    plt.xlabel("z")
    plt.ylabel("Hy")
    plt.grid()
    plt.show()
    return z_eler, hy_eler, points

def kes_dist(z_w, b, c, pds_p, z_zakr, hy_zakr, len_zakr, z_eler, hy_eler, len_eler, z, hy):
    hy_full=interpolating_spline(1,sx,z_w,hy)
    sp_hy_zakr=interpolating_spline(1,sx, z_zakr, hy_zakr)
    sp_hy_eler=interpolating_spline(1,sx, z_eler, hy_eler)
    hy_1=[]
    hy_2=[]
    for i in np.linspace(z_w[0],z_w[0]+len_zakr, 100):
        hy_1.append(hy_full.subs(sx,i)-sp_hy_zakr.subs(sx,i))
    for i in np.linspace(z_w[len(z_w)-1]-len_eler,z_w[len(z_w)-1], 100):
        hy_2.append(hy_full.subs(sx,i)-sp_hy_eler.subs(sx,i))
    hy_kes=hy_1+hy_2
    z_kes=np.linspace(z_w[0],z_w[0]+len_zakr, 100)
    z_kes=np.append(z_kes, np.linspace(z_w[len(z_w)-1]-len_eler,z_w[len(z_w)-1], 100))

    plt.plot(z_kes, hy_kes)
    plt.plot(np.linspace(z_w[0],z_w[0]+len_zakr, 100), hy_1)
    plt.plot(np.linspace(z_w[len(z_w)-1]-len_eler,z_w[len(z_w)-1], 100), hy_2)
    plt.plot(z_kes[:100], hy_1)
    plt.xlabel("z")
    plt.ylabel("Hy")
    plt.grid()
    plt.show()
    return z_kes, hy_kes


# In[ ]:




