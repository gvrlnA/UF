#!/usr/bin/env python
# coding: utf-8

# In[13]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import Rbf

def mass_distribution_func(i):
    if i==0: #крыло
        z_start = 0.78
        z_finish = 8.27
    if i==1: #элерон
        z_finish = 8.27
        z_start = z_finish - 2.974
    if i==2: #закрылок
        z_start = 0.78
        z_finish = z_start + 4.515
    
    mass_distribution = pd.read_excel('Распределение_масс_крыло.xlsx',sheet_name=i, index_col=0)

    m = np.array(mass_distribution['Масса, кгс'].tolist())
    x = np.array(mass_distribution['X, м'].tolist())
    z = np.array(mass_distribution['Z, м'].tolist())
    ny = np.array(mass_distribution['Расчетная перегрузка'].head(1).tolist())

    # Create a radial basis function interpolation
    rbf = Rbf(z, x, m)

    # Evaluate the interpolation at new points
    new_z = np.linspace(0.7, 8.27, 7570)
    new_x = np.linspace(min(x), max(x), 7570)
    new_m = rbf(new_z, new_x)
    for i in range(len(new_m)-1, -1, -1):
        if (new_m[i]<=0) or (new_z[i]<z_start) or (new_z[i]>z_finish):
            new_m = np.delete(new_m, i)
            new_z = np.delete(new_z, i)
            new_x = np.delete(new_x, i)
    
    new_m = ny*new_m
    
    get_ipython().run_line_magic('matplotlib', 'widget')

    # Create 3D plot of the data points and the fitted curve 
    fig = plt.figure(figsize=(10,10)) 
    ax = fig.add_subplot(111, projection='3d') 
    ax.scatter(new_z, new_x, new_m, cmap='jet') 
    ax.set_xlabel('Z') 
    ax.set_ylabel('X') 
    ax.set_zlabel('M') 
    plt.show()
    return new_m, new_z, new_x


# In[ ]:




