#!/usr/bin/env python
# coding: utf-8

# In[13]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import Rbf

def mass_distribution_func(file_name, absc_ax_name, ord_ax_name, i):
    if i==0: #крыло
        z_start = 0.78
        z_finish = 8.27
    if i==1: #элерон
        z_finish = 8.27
        z_start = z_finish - 2.974
    if i==2: #закрылок
        z_start = 0.78
        z_finish = z_start + 4.515
    
    mass_distribution = pd.read_excel(file_name, sheet_name=i, index_col=0)

    m = np.array(mass_distribution['Масса, кгс'].tolist())
    absc = np.array(mass_distribution[absc_ax_name].tolist())
    ordi = np.array(mass_distribution[ord_ax_name].tolist())
    ny = np.array(mass_distribution['Расчетная перегрузка'].head(1).tolist())

    # Create a radial basis function interpolation
    rbf = Rbf(ordi, absc, m)

    # Evaluate the interpolation at new points
    new_ordi = np.linspace(0.7, 8.27, 7570)
    new_absc = np.linspace(min(absc), max(absc), 7570)
    new_m = rbf(new_ordi, new_absc)
    for i in range(len(new_m)-1, -1, -1):
        if (new_m[i]<=0) or (new_ordi[i]<z_start) or (new_ordi[i]>z_finish):
            new_m = np.delete(new_m, i)
            new_ordi = np.delete(new_ordi, i)
            new_absc = np.delete(new_absc, i)
    
    new_m = ny*new_m
    
    get_ipython().run_line_magic('matplotlib', 'widget')

    # Create 3D plot of the data points and the fitted curve 
    fig = plt.figure(figsize=(10,10)) 
    ax = fig.add_subplot(111, projection='3d') 
    ax.scatter(new_ordi, new_absc, new_m, cmap='jet') 
    ax.set_xlabel(ord_ax_name) 
    ax.set_ylabel(absc_ax_name) 
    ax.set_zlabel('Масса, кгс') 
    plt.show()
    return new_m, new_ordi, new_absc


# In[ ]:




