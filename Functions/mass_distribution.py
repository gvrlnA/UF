#!/usr/bin/env python
# coding: utf-8

# In[13]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import Rbf
import Geometry_for_time as gl

def mass_distribution_func(file_name, absc_ax_name, dep, ord_ax_name, var, sheet_name, start_ord, finish_ord):
    
    Front, Back, Front_line, Back_line = gl.geometry(sheet_name, var, dep)
    absc_start, absc_finish = gl.boundary_points(Front_line, Back_line, var)
    absc_start, absc_finish = round(absc_start/1000, 3), round(absc_finish/1000, 3)
    
    mass_distribution = pd.read_excel(file_name, sheet_name=sheet_name, index_col=0)

    m = np.array(mass_distribution['Масса, кгс'].tolist())
    absc = np.array(mass_distribution[absc_ax_name].tolist())
    ordi = np.array(mass_distribution[ord_ax_name].tolist())
    ny = np.array(mass_distribution['Расчетная перегрузка'].head(1).tolist())

    # Create a radial basis function interpolation
    rbf = Rbf(ordi, absc, m)
    
    # Evaluate the interpolation at new points
    new_ordi = np.linspace(round(start_ord/1000, 3), round(finish_ord/1000, 3), int(round(finish_ord - start_ord)))
    new_absc = np.linspace(min(absc), max(absc), int(round(finish_ord - start_ord)))
    new_m = rbf(new_ordi, new_absc)
    for i in range(len(new_m)-1, -1, -1):
        if (new_m[i]<=0) or (new_ordi[i]<absc_start) or (new_ordi[i]>absc_finish):
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




