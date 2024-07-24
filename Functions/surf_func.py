#!/usr/bin/env python
# coding: utf-8

# In[17]:


import pandas as pd
import numpy as np
from scipy import *
from sympy import *
import math as mp
from scipy.linalg import solve
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit 
import openpyxl
from scipy.interpolate import LinearNDInterpolator


# In[18]:


def MakingSurface(file_straps_cord, workbook):
    #(file_straps_cord - имя файла с кооринатами лямок, workbook - имя файла с распределениями и шаблонами для записи)
    
    sheet_names = pd.ExcelFile(workbook).sheet_names
    dis_p = pd.read_excel(workbook, sheet_name=sheet_names[0], index_col=0)
    
    """Верхняя часть"""

    dis_p_data = [[[], []] for _ in range(int((len(dis_p.columns)-1)/2))]

    x, z, p =[], [], []

    """Запись z сечений"""
    z_list = dis_p['z, м'].tolist()
    z_list = [x for x in z_list if str(x) != 'nan']

    """Запись X"""
    list_dis_p_x = dis_p.iloc[:, 0:(len(z_list)*2):2].values.tolist()
    for i in range(len(list_dis_p_x[0])):
        for j in range(len(list_dis_p_x)):
            dis_p_data[i][0].append(list_dis_p_x[j][i])

    """Запись p"""
    list_dis_p = dis_p.iloc[:, 1:(len(z_list)*2):2].values.tolist()
    for i in range(len(list_dis_p[0])):
        for j in range(len(list_dis_p)):
            dis_p_data[i][1].append(list_dis_p[j][i])

    num_points_sec = int(len([x for x in dis_p.iloc[:, 0].values.tolist() if str(x) != 'nan'])/2) #the number of points in the section
            
    for i in range(len(z_list)):
        for j in range(num_points_sec):
            x.append(list_dis_p_x[j][i])
            z.append(z_list[i])
            p.append(list_dis_p[j][i])

    X = np.linspace(min(x), max(x), num=num_points_sec)
    Z = np.linspace(min(z), max(z), num=int((max(z)-min(z))*1000))
    X, Z = np.meshgrid(X, Z)
    # Interpolate the z values on the meshgrid
    interp = LinearNDInterpolator(list(zip(x, z)), p)
    P = interp(X, Z)
    fig = plt.figure(figsize=(10,10)) 
    plt.pcolormesh(X, Z, P, shading='auto')
    plt.plot(x, z, "ok", label="input point")
    plt.legend()
    plt.colorbar()
    plt.axis("equal")
    plt.show()

    straps_cord = pd.read_excel(file_straps_cord, sheet_name=pd.ExcelFile(file_straps_cord).sheet_names[0], index_col=0)

    z_centre = list(straps_cord.loc['Координаты по Z:'])
    z_centre = [z_centre[i]/1000 for i in range(len(z_centre))]

    #horda kryla
    sz = symbols('z')
    PK=[0.824, 0.0, 0.0, 0.0, 0.0, 0.824]
    z_PK=[-8.27, -4.558, -0.78, 0.78, 4.558, 8.27]
    BK=[1.824, 2.0, 2.0, 2.0, 2.0, 1.824]
    z_BK=[-8.27, -5.27, -0.78, 0.78,5.27,8.27]
    spl_PK=interpolating_spline(1, sz, z_PK, PK)
    spl_BK=interpolating_spline(1, sz, z_BK, BK)
    b = interpolating_spline(1, sz, z_BK, BK)-interpolating_spline(1, sz, z_PK, PK)

    x_s, z_s, p_s = [], [], []

    for i in range(len(z_centre)):
        for j in range(len(Z)):
            if round(z_centre[i]*1000)==round(Z[j][0]*1000):
                for k in range(num_points_sec):
                    x_s.append(X[j][k])
                    z_s.append(z_centre[i])
                    p_s.append(P[j][k])

    # Выбираем нужный лист
    wb = openpyxl.load_workbook(workbook)
    worksheet = wb[sheet_names[1]]

    for i in range(len(z_centre)):
        c = worksheet.cell(row=1, column=(2*i)+2)
        c.value = "x=" + str(z_centre[i])
        c = worksheet.cell(row=1, column=(2*i+1)+2)
        c.value = "p=" + str(z_centre[i])
        for j in range(num_points_sec):
            c = worksheet.cell(row=j+2, column=(2*i)+2)
            c.value = x_s[i*num_points_sec+j]
            c = worksheet.cell(row=j+2, column=(2*i+1)+2)
            c.value = p_s[i*num_points_sec+j]
    
    for l in range(2, len(sheet_names)):
        z_type = pd.read_excel(file_straps_cord, sheet_name=sheet_names[l], index_col=0)
        z_type_list = list(z_type.loc['Координаты по Z:'])
        z_type_list = [z_type_list[i]/1000 for i in range(len(z_type_list))]
        # Выбираем нужный лист
        worksheet = wb[sheet_names[l]]
        for i in range(len(z_centre)):
            for k in range(len((z_type_list))):
                if z_type_list[k]==z_centre[i]:
                    c = worksheet.cell(row=1, column=(2*i)+2)
                    c.value = z_type_list[k]
                    c = worksheet.cell(row=1, column=(2*i+1)+2)
                    c.value = z_type_list[k]
                    for j in range(num_points_sec):
                        c = worksheet.cell(row=j+2, column=(2*i)+2)
                        c.value = x_s[i*num_points_sec+j]
                        c = worksheet .cell(row=j+2, column=(2*i+1)+2)
                        c.value = p_s[i*num_points_sec+j]

    """Нижняя часть"""
     
    dis_p_data = [[[], []] for _ in range(int((len(dis_p.columns)-1)/2))]

    x, z, p =[], [], []

    """Запись X"""
    list_dis_p_x = dis_p.iloc[:, 0:(len(z_list)*2):2].values.tolist()
    for i in range(len(list_dis_p_x[0])):
        for j in range(len(list_dis_p_x)):
            dis_p_data[i][0].append(list_dis_p_x[j][i])

    """Запись p"""
    list_dis_p = dis_p.iloc[:, 1:(len(z_list)*2):2].values.tolist()
    for i in range(len(list_dis_p[0])):
        for j in range(len(list_dis_p)):
            dis_p_data[i][1].append(list_dis_p[j][i])
            
    for i in range(len(z_list)):
        for j in range(num_points_sec, num_points_sec*2):
            x.append(list_dis_p_x[j][i])
            z.append(z_list[i])
            p.append(list_dis_p[j][i])

    X = np.linspace(min(x), max(x), num=num_points_sec)
    Z = np.linspace(min(z), max(z), num=int((max(z)-min(z))*1000))
    X, Z = np.meshgrid(X, Z)
    # Interpolate the z values on the meshgrid
    interp = LinearNDInterpolator(list(zip(x, z)), p)
    P = interp(X, Z)
    fig = plt.figure(figsize=(10,10)) 
    plt.pcolormesh(X, Z, P, shading='auto')
    plt.plot(x, z, "ok", label="input point")
    plt.legend()
    plt.colorbar()
    plt.axis("equal")
    plt.show()

    x_s, z_s, p_s = [], [], []

    for i in range(len(z_centre)):
        for j in range(len(Z)):
            if round(z_centre[i]*1000)==round(Z[j][0]*1000):
                for k in range(num_points_sec):
                    x_s.append(X[j][k])
                    z_s.append(z_centre[i])
                    p_s.append(P[j][k])
    
    worksheet = wb[sheet_names[1]]
    
    for i in range(len(z_centre)):
        for j in range(num_points_sec):
            c = worksheet.cell(row=j+2+num_points_sec, column=(2*i)+2)
            c.value = x_s[i*num_points_sec+j]
            c = worksheet.cell(row=j+2+num_points_sec, column=(2*i+1)+2)
            c.value = p_s[i*num_points_sec+j]
    
    for l in range(2, len(sheet_names)):
        z_type = pd.read_excel(file_straps_cord, sheet_name=sheet_names[l], index_col=0)
        z_type_list = list(z_type.loc['Координаты по Z:'])
        z_type_list = [z_type_list[i]/1000 for i in range(len(z_type_list))]
        # Выбираем нужный лист
        worksheet = wb[sheet_names[l]]
        for i in range(len(z_centre)):
            for k in range(len((z_type_list))):
                if z_type_list[k]==z_centre[i]:
                    for j in range(num_points_sec):
                        c = worksheet.cell(row=j+2+num_points_sec, column=(2*i)+2)
                        c.value = x_s[i*num_points_sec+j]
                        c = worksheet.cell(row=j+2+num_points_sec, column=(2*i+1)+2)
                        c.value = p_s[i*num_points_sec+j]

    # Сохраняем изменения в файле
    wb.save('Распределение_давлений_по_хордам_с_лямками_Аштрих.xlsx')


# In[ ]:




