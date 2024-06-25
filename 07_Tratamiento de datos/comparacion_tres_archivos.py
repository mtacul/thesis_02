# -*- coding: utf-8 -*-
"""
Created on Sun Jun 23 22:39:30 2024

@author: nachi
"""

#%% Librerias a utilizar
import matplotlib.pyplot as plt
import pandas as pd
import functions
from scipy.signal import welch
import numpy as np
import scipy.stats as stats
import os

#%%

# Definir la lista de archivos CSV disponibles
archivos_disponibles = [
    "_sen1_act1_RW_2.csv",
    "_sen1_act2_RW_2.csv",
    "_sen1_act3_RW_2.csv",
    "_sen2_act1_RW_2.csv",
    "_sen2_act2_RW_2.csv",
    "_sen2_act3_RW_2.csv",
    "_sen3_act1_RW_2.csv",
    "_sen3_act2_RW_2.csv",
    "_sen3_act3_RW_2.csv",
    "_sen1_act1_MT.csv",
    "_sen1_act2_MT.csv",
    "_sen1_act3_MT.csv",
    "_sen2_act1_MT.csv",
    "_sen2_act2_MT.csv",
    "_sen2_act3_MT.csv",
    "_sen3_act1_MT.csv",
    "_sen3_act2_MT.csv",
    "_sen3_act3_MT.csv"
    ]

# Mostrar el menú al usuario
print("Seleccione tres archivos CSV para abrir:")
for i, archivo in enumerate(archivos_disponibles, 1):
    print(f"{i}. {archivo}")

# Obtener las elecciones del usuario
opciones = input("Ingrese los números de los archivos deseados, separados por comas: ").split(',')

# Validar las opciones del usuario
opciones = [int(opcion.strip()) for opcion in opciones if opcion.strip().isdigit()]

if all(1 <= opcion <= len(archivos_disponibles) for opcion in opciones) and len(opciones) == 3:
    archivos_seleccionados = [archivos_disponibles[opcion - 1] for opcion in opciones]
    
    # Leer los archivos CSV en DataFrames de pandas
    dataframes = [pd.read_csv(archivo) for archivo in archivos_seleccionados]
    
    # Convertir los DataFrames a arrays de NumPy
    arrays_datos = [df.to_numpy() for df in dataframes]
    
    # Ahora puedes usar 'arrays_datos' en tu código
    print("Archivos seleccionados:")
    for archivo in archivos_seleccionados:
        print(archivo)
else:
    print("Opciones inválidas. Por favor, ingrese tres números válidos.")
    
print("\n")

array_datos_1 = arrays_datos[0]
array_datos_2 = arrays_datos[1]
array_datos_3 = arrays_datos[2]

t_aux = array_datos_1[:,0]
Roll_1 = array_datos_1[:,1]
Pitch_1 =  array_datos_1[:,2]
Yaw_1 =  array_datos_1[:,3]
q0_real_1 = array_datos_1[:,4]
q1_real_1 = array_datos_1[:,5]
q2_real_1 = array_datos_1[:,6]
q3_real_1 = array_datos_1[:,7]
q0_est_1 = array_datos_1[:,8]
q1_est_1 = array_datos_1[:,9]
q2_est_1 = array_datos_1[:,10]
q3_est_1 = array_datos_1[:,11]
w0_est_1 = array_datos_1[:,12]
w1_est_1 = array_datos_1[:,13]
w2_est_1 = array_datos_1[:,14]
Roll_low_pass_1 = array_datos_1[:,18]
Pitch_low_pass_1 =  array_datos_1[:,19]
Yaw_low_pass_1 =  array_datos_1[:,20]

Roll_2 = array_datos_2[:,1]
Pitch_2 =  array_datos_2[:,2]
Yaw_2 =  array_datos_2[:,3]
q0_real_2 = array_datos_2[:,4]
q1_real_2 = array_datos_2[:,5]
q2_real_2 = array_datos_2[:,6]
q3_real_2 = array_datos_2[:,7]
q0_est_2 = array_datos_2[:,8]
q1_est_2 = array_datos_2[:,9]
q2_est_2 = array_datos_2[:,10]
q3_est_2 = array_datos_2[:,11]
w0_est_2 = array_datos_2[:,12]
w1_est_2 = array_datos_2[:,13]
w2_est_2 = array_datos_2[:,14]
Roll_low_pass_2 = array_datos_2[:,18]
Pitch_low_pass_2 =  array_datos_2[:,19]
Yaw_low_pass_2 =  array_datos_2[:,20]

Roll_3 = array_datos_3[:,1]
Pitch_3 =  array_datos_3[:,2]
Yaw_3 =  array_datos_3[:,3]
q0_real_3 = array_datos_3[:,4]
q1_real_3 = array_datos_3[:,5]
q2_real_3 = array_datos_3[:,6]
q3_real_3 = array_datos_3[:,7]
q0_est_3 = array_datos_3[:,8]
q1_est_3 = array_datos_3[:,9]
q2_est_3 = array_datos_3[:,10]
q3_est_3 = array_datos_3[:,11]
w0_est_3 = array_datos_3[:,12]
w1_est_3 = array_datos_3[:,13]
w2_est_3 = array_datos_3[:,14]
Roll_low_pass_3 = array_datos_3[:,18]
Pitch_low_pass_3 =  array_datos_3[:,19]
Yaw_low_pass_3 =  array_datos_3[:,20]

#%% Densidad espectro potencia para el jitter

#Filtro pasa alto para el Jitter y pasa bajo para exactitud de apuntamiento y agilidad
Roll_high_pass_1 = functions.high_pass_filter(Roll_1, 10, len(t_aux))
Pitch_high_pass_1 = functions.high_pass_filter(Pitch_1, 10, len(t_aux))
Yaw_high_pass_1 = functions.high_pass_filter(Yaw_1, 10, len(t_aux))

frequencies_R_1, psd_R_1 = welch(Roll_high_pass_1, len(t_aux), nperseg=1024)
frequencies_P_1, psd_P_1 = welch(Pitch_high_pass_1, len(t_aux), nperseg=1024)
frequencies_Y_1, psd_Y_1 = welch(Yaw_high_pass_1, len(t_aux), nperseg=1024)

psd_R_R_1 =[]
psd_P_R_1 =[]
psd_Y_R_1 =[]

for i in range(len(frequencies_R_1)):
    psd_R_r_1 = np.real(psd_R_1[i])
    psd_P_r_1 = np.real(psd_P_1[i])
    psd_Y_r_1 = np.real(psd_Y_1[i])
    psd_R_R_1.append(psd_R_r_1)
    psd_P_R_1.append(psd_P_r_1)
    psd_Y_R_1.append(psd_Y_r_1)

psd_R_R_1 = np.array(psd_R_R_1)
psd_P_R_1 = np.array(psd_P_R_1)
psd_Y_R_1 = np.array(psd_Y_R_1)

# Definir los anchos de banda deseados
bandwidth_1 = (0, 10000)  # Ancho de banda 1 en Hz

# Calcular la PSD dentro de los anchos de banda específicos
indices_bandwidth_1_R = np.where((frequencies_R_1 >= bandwidth_1[0]) & (frequencies_R_1 <= bandwidth_1[1]))
psd_bandwidth_1_R = np.trapz(psd_R_1[indices_bandwidth_1_R], frequencies_R_1[indices_bandwidth_1_R])

indices_bandwidth_1_P = np.where((frequencies_P_1 >= bandwidth_1[0]) & (frequencies_P_1 <= bandwidth_1[1]))
psd_bandwidth_1_P = np.trapz(psd_P_1[indices_bandwidth_1_P], frequencies_P_1[indices_bandwidth_1_P])

indices_bandwidth_1_Y = np.where((frequencies_Y_1 >= bandwidth_1[0]) & (frequencies_Y_1 <= bandwidth_1[1]))
psd_bandwidth_1_Y = np.trapz(psd_Y_1[indices_bandwidth_1_Y], frequencies_Y_1[indices_bandwidth_1_Y])

psd_RPY_1 = np.array([psd_bandwidth_1_R,psd_bandwidth_1_P,psd_bandwidth_1_Y])


#Filtro pasa alto para el Jitter y pasa bajo para exactitud de apuntamiento y agilidad
Roll_high_pass_2 = functions.high_pass_filter(Roll_2, 10, len(t_aux))
Pitch_high_pass_2 = functions.high_pass_filter(Pitch_2, 10, len(t_aux))
Yaw_high_pass_2 = functions.high_pass_filter(Yaw_2, 10, len(t_aux))

frequencies_R_2, psd_R_2 = welch(Roll_high_pass_2, len(t_aux), nperseg=1024)
frequencies_P_2, psd_P_2 = welch(Pitch_high_pass_2, len(t_aux), nperseg=1024)
frequencies_Y_2, psd_Y_2 = welch(Yaw_high_pass_2, len(t_aux), nperseg=1024)

psd_R_R_2 =[]
psd_P_R_2 =[]
psd_Y_R_2 =[]

for i in range(len(frequencies_R_2)):
    psd_R_r_2 = np.real(psd_R_2[i])
    psd_P_r_2 = np.real(psd_P_2[i])
    psd_Y_r_2 = np.real(psd_Y_2[i])
    psd_R_R_2.append(psd_R_r_2)
    psd_P_R_2.append(psd_P_r_2)
    psd_Y_R_2.append(psd_Y_r_2)

psd_R_R_2 = np.array(psd_R_R_2)
psd_P_R_2 = np.array(psd_P_R_2)
psd_Y_R_2 = np.array(psd_Y_R_2)

# Definir los anchos de banda deseados
bandwidth_2 = (0, 10000)  # Ancho de banda 1 en Hz

# Calcular la PSD dentro de los anchos de banda específicos
indices_bandwidth_2_R = np.where((frequencies_R_2 >= bandwidth_2[0]) & (frequencies_R_2 <= bandwidth_2[1]))
psd_bandwidth_2_R = np.trapz(psd_R_2[indices_bandwidth_2_R], frequencies_R_2[indices_bandwidth_2_R])

indices_bandwidth_2_P = np.where((frequencies_P_2 >= bandwidth_2[0]) & (frequencies_P_2 <= bandwidth_2[1]))
psd_bandwidth_2_P = np.trapz(psd_P_2[indices_bandwidth_2_P], frequencies_P_2[indices_bandwidth_2_P])

indices_bandwidth_2_Y = np.where((frequencies_Y_2 >= bandwidth_2[0]) & (frequencies_Y_2 <= bandwidth_2[1]))
psd_bandwidth_2_Y = np.trapz(psd_Y_2[indices_bandwidth_2_Y], frequencies_Y_2[indices_bandwidth_2_Y])

psd_RPY_2 = np.array([psd_bandwidth_2_R,psd_bandwidth_2_P,psd_bandwidth_2_Y])


#Filtro pasa alto para el Jitter y pasa bajo para exactitud de apuntamiento y agilidad
Roll_high_pass_3 = functions.high_pass_filter(Roll_3, 10, len(t_aux))
Pitch_high_pass_3 = functions.high_pass_filter(Pitch_3, 10, len(t_aux))
Yaw_high_pass_3 = functions.high_pass_filter(Yaw_3, 10, len(t_aux))

frequencies_R_3, psd_R_3 = welch(Roll_high_pass_3, len(t_aux), nperseg=1024)
frequencies_P_3, psd_P_3 = welch(Pitch_high_pass_3, len(t_aux), nperseg=1024)
frequencies_Y_3, psd_Y_3 = welch(Yaw_high_pass_3, len(t_aux), nperseg=1024)

psd_R_R_3 =[]
psd_P_R_3 =[]
psd_Y_R_3 =[]

for i in range(len(frequencies_R_3)):
    psd_R_r_3 = np.real(psd_R_3[i])
    psd_P_r_3 = np.real(psd_P_3[i])
    psd_Y_r_3 = np.real(psd_Y_3[i])
    psd_R_R_3.append(psd_R_r_3)
    psd_P_R_3.append(psd_P_r_3)
    psd_Y_R_3.append(psd_Y_r_3)

psd_R_R_3 = np.array(psd_R_R_3)
psd_P_R_3 = np.array(psd_P_R_3)
psd_Y_R_3 = np.array(psd_Y_R_3)

# Definir los anchos de banda deseados
bandwidth_3 = (0, 10000)  # Ancho de banda 1 en Hz

# Calcular la PSD dentro de los anchos de banda específicos
indices_bandwidth_3_R = np.where((frequencies_R_3 >= bandwidth_3[0]) & (frequencies_R_3 <= bandwidth_3[1]))
psd_bandwidth_3_R = np.trapz(psd_R_3[indices_bandwidth_3_R], frequencies_R_3[indices_bandwidth_3_R])

indices_bandwidth_3_P = np.where((frequencies_P_3 >= bandwidth_3[0]) & (frequencies_P_3 <= bandwidth_3[1]))
psd_bandwidth_3_P = np.trapz(psd_P_3[indices_bandwidth_3_P], frequencies_P_3[indices_bandwidth_3_P])

indices_bandwidth_3_Y = np.where((frequencies_Y_3 >= bandwidth_3[0]) & (frequencies_Y_3 <= bandwidth_3[1]))
psd_bandwidth_3_Y = np.trapz(psd_Y_3[indices_bandwidth_3_Y], frequencies_Y_3[indices_bandwidth_3_Y])

psd_RPY_3 = np.array([psd_bandwidth_3_R,psd_bandwidth_3_P,psd_bandwidth_3_Y])

#%% Encontrar el tiempo de asentamiento en segundos de cada angulo de Euler

settling_band_R = 5
settling_band_P = 5
settling_band_Y = 5

settling_error_sup_R = np.full(len(t_aux),settling_band_R)
settling_error_inf_R = np.full(len(t_aux),-settling_band_R)

settling_error_sup_P = np.full(len(t_aux),settling_band_P)
settling_error_inf_P = np.full(len(t_aux),-settling_band_P)

settling_error_sup_Y = np.full(len(t_aux),settling_band_Y)
settling_error_inf_Y = np.full(len(t_aux),-settling_band_Y)

#%% Asentamientos para la opcion 1

settling_time_indices_R_1 = []
start_index_R_1 = None
settling_time_indices_P_1 = []
start_index_P_1 = None
settling_time_indices_Y_1 = []
start_index_Y_1 = None


for i in range(len(Roll_low_pass_1)):
    if Roll_low_pass_1[i] <= settling_error_sup_R[i] and Roll_low_pass_1[i] >= settling_error_inf_R[i]:
        if start_index_R_1 is None:
            start_index_R_1 = i
    else:
        if start_index_R_1 is not None:
            settling_time_indices_R_1.append((start_index_R_1, i - 1))
            start_index_R_1 = None

if start_index_R_1 is not None:
    settling_time_indices_R_1.append((start_index_R_1, len(Roll_low_pass_1) - 1))

if settling_time_indices_R_1:
    settling_times_R_1 = []
    for start, end in settling_time_indices_R_1:
        settling_times_R_1.append((t_aux[start], t_aux[end]))
else:
    print("La señal no entra en la banda de asentamiento.")
    

for i in range(len(Pitch_low_pass_1)):
    if Pitch_low_pass_1[i] <= settling_error_sup_P[i] and Pitch_low_pass_1[i] >= settling_error_inf_P[i]:
        if start_index_P_1 is None:
            start_index_P_1 = i
    else:
        if start_index_P_1 is not None:
            settling_time_indices_P_1.append((start_index_P_1, i - 1))
            start_index_P_1 = None

if start_index_P_1 is not None:
    settling_time_indices_P_1.append((start_index_P_1, len(Pitch_low_pass_1) - 1))

if settling_time_indices_P_1:
    settling_times_P_1 = []
    for start, end in settling_time_indices_P_1:
        settling_times_P_1.append((t_aux[start], t_aux[end]))
else:
    print("La señal no entra en la banda de asentamiento.")


for i in range(len(Yaw_low_pass_1)):
    if Yaw_low_pass_1[i] <= settling_error_sup_Y[i] and Yaw_low_pass_1[i] >= settling_error_inf_Y[i]:
        if start_index_Y_1 is None:
            start_index_Y_1 = i
    else:
        if start_index_Y_1 is not None:
            settling_time_indices_Y_1.append((start_index_Y_1, i - 1))
            start_index_Y_1 = None

if start_index_Y_1 is not None:
    settling_time_indices_Y_1.append((start_index_Y_1, len(Yaw_low_pass_1) - 1))

if settling_time_indices_Y_1:
    settling_times_Y_1 = []
    for start, end in settling_time_indices_Y_1:
        settling_times_Y_1.append((t_aux[start], t_aux[end]))
else:
    print("La señal no entra en la banda de asentamiento.")


#%% Asentamientos para la opcion 2

settling_time_indices_R_2 = []
start_index_R_2 = None
settling_time_indices_P_2 = []
start_index_P_2 = None
settling_time_indices_Y_2 = []
start_index_Y_2 = None


for i in range(len(Roll_low_pass_2)):
    if Roll_low_pass_2[i] <= settling_error_sup_R[i] and Roll_low_pass_2[i] >= settling_error_inf_R[i]:
        if start_index_R_2 is None:
            start_index_R_2 = i
    else:
        if start_index_R_2 is not None:
            settling_time_indices_R_2.append((start_index_R_2, i - 1))
            start_index_R_2 = None

if start_index_R_2 is not None:
    settling_time_indices_R_2.append((start_index_R_2, len(Roll_low_pass_2) - 1))

if settling_time_indices_R_2:
    settling_times_R_2 = []
    for start, end in settling_time_indices_R_2:
        settling_times_R_2.append((t_aux[start], t_aux[end]))
else:
    print("La señal no entra en la banda de asentamiento.")
        
    
for i in range(len(Pitch_low_pass_2)):
    if Pitch_low_pass_2[i] <= settling_error_sup_P[i] and Pitch_low_pass_2[i] >= settling_error_inf_P[i]:
        if start_index_P_2 is None:
            start_index_P_2 = i
    else:
        if start_index_P_2 is not None:
            settling_time_indices_P_2.append((start_index_P_2, i - 1))
            start_index_P_2 = None

if start_index_P_2 is not None:
    settling_time_indices_P_2.append((start_index_P_2, len(Pitch_low_pass_2) - 1))

if settling_time_indices_P_2:
    settling_times_P_2 = []
    for start, end in settling_time_indices_P_2:
        settling_times_P_2.append((t_aux[start], t_aux[end]))
else:
    print("La señal no entra en la banda de asentamiento.")


for i in range(len(Yaw_low_pass_2)):
    if Yaw_low_pass_2[i] <= settling_error_sup_Y[i] and Yaw_low_pass_2[i] >= settling_error_inf_Y[i]:
        if start_index_Y_2 is None:
            start_index_Y_2 = i
    else:
        if start_index_Y_2 is not None:
            settling_time_indices_Y_2.append((start_index_Y_2, i - 1))
            start_index_Y_2 = None

if start_index_Y_2 is not None:
    settling_time_indices_Y_2.append((start_index_Y_2, len(Yaw_low_pass_2) - 1))

if settling_time_indices_Y_2:
    settling_times_Y_2 = []
    for start, end in settling_time_indices_Y_2:
        settling_times_Y_2.append((t_aux[start], t_aux[end]))
else:
    print("La señal no entra en la banda de asentamiento.")


#%% Asentamiento para la opcion 3

settling_time_indices_R_3 = []
start_index_R_3= None
settling_time_indices_P_3 = []
start_index_P_3 = None
settling_time_indices_Y_3 = []
start_index_Y_3 = None

for i in range(len(Roll_low_pass_3)):
    if Roll_low_pass_3[i] <= settling_error_sup_R[i] and Roll_low_pass_3[i] >= settling_error_inf_R[i]:
        if start_index_R_3 is None:
            start_index_R_3 = i
    else:
        if start_index_R_3 is not None:
            settling_time_indices_R_3.append((start_index_R_3, i - 1))
            start_index_R_3 = None

if start_index_R_3 is not None:
    settling_time_indices_R_3.append((start_index_R_3, len(Roll_low_pass_3) - 1))

if settling_time_indices_R_3:
    settling_times_R_3 = []
    for start, end in settling_time_indices_R_3:
        settling_times_R_3.append((t_aux[start], t_aux[end]))
else:
    print("La señal no entra en la banda de asentamiento.")
    


for i in range(len(Pitch_low_pass_3)):
    if Pitch_low_pass_3[i] <= settling_error_sup_P[i] and Pitch_low_pass_3[i] >= settling_error_inf_P[i]:
        if start_index_P_3 is None:
            start_index_P_3 = i
    else:
        if start_index_P_3 is not None:
            settling_time_indices_P_3.append((start_index_P_3, i - 1))
            start_index_P_3 = None

if start_index_P_3 is not None:
    settling_time_indices_P_3.append((start_index_P_3, len(Pitch_low_pass_3) - 1))

if settling_time_indices_P_3:
    settling_times_P_3 = []
    for start, end in settling_time_indices_P_3:
        settling_times_P_3.append((t_aux[start], t_aux[end]))
else:
    print("La señal no entra en la banda de asentamiento.")



for i in range(len(Yaw_low_pass_3)):
    if Yaw_low_pass_3[i] <= settling_error_sup_Y[i] and Yaw_low_pass_3[i] >= settling_error_inf_Y[i]:
        if start_index_Y_3 is None:
            start_index_Y_3 = i
    else:
        if start_index_Y_3 is not None:
            settling_time_indices_Y_3.append((start_index_Y_3, i - 1))
            start_index_Y_3 = None

if start_index_Y_3 is not None:
    settling_time_indices_Y_3.append((start_index_Y_3, len(Yaw_low_pass_3) - 1))

if settling_time_indices_Y_3:
    settling_times_Y_3 = []
    for start, end in settling_time_indices_Y_3:
        settling_times_Y_3.append((t_aux[start], t_aux[end]))
else:
    print("La señal no entra en la banda de asentamiento.")

# print("\n")

#%% Exactitud de apuntamiento

time_R_1 = np.array(settling_times_R_1[-1])
data_R_1 = Roll_1[int(time_R_1[0]/2):int(time_R_1[1]/2)]
# Calcular media y desviación estándar
media_R_1 = np.mean(data_R_1)
sigma_R_1 = np.std(data_R_1)
# Calcular los límites de 3 sigma
lim_inf_R_1 = media_R_1 - 3 * sigma_R_1
lim_sup_R_1 = media_R_1 + 3 * sigma_R_1
accuracy_R_1 = 3*sigma_R_1

time_P_1 = np.array(settling_times_P_1[-1])
data_P_1 = Pitch_1[int(time_P_1[0]/2):int(time_P_1[1]/2)]
# Calcular media y desviación estándar
media_P_1 = np.mean(data_P_1)
sigma_P_1 = np.std(data_P_1)
# Calcular los límites de 3 sigma
lim_inf_P_1 = media_P_1 - 3 * sigma_P_1
lim_sup_P_1 = media_P_1 + 3 * sigma_P_1
accuracy_P_1 = 3*sigma_P_1

time_Y_1 = np.array(settling_times_Y_1[-1])
data_Y_1= Yaw_1[int(time_Y_1[0]/2):int(time_Y_1[1]/2)]
# Calcular media y desviación estándar
media_Y_1 = np.mean(data_Y_1)
sigma_Y_1 = np.std(data_Y_1)
# Calcular los límites de 3 sigma
lim_inf_Y_1 = media_Y_1 - 3 * sigma_Y_1
lim_sup_Y_1 = media_Y_1 + 3 * sigma_Y_1
accuracy_Y_1 = 3*sigma_Y_1

accuracy_RPY_1 = np.array([accuracy_R_1,accuracy_P_1,accuracy_Y_1])
# print("La exactitud de apuntamiento para Roll, Pitch y Yaw son respecticamente: \n", accuracy_RPY_1, "[°]")


time_R_2 = np.array(settling_times_R_2[-1])
data_R_2 = Roll_2[int(time_R_2[0]/2):int(time_R_2[1]/2)]
# Calcular media y desviación estándar
media_R_2 = np.mean(data_R_2)
sigma_R_2 = np.std(data_R_2)
# Calcular los límites de 3 sigma
lim_inf_R_2 = media_R_2 - 3 * sigma_R_2
lim_sup_R_2 = media_R_2 + 3 * sigma_R_2
accuracy_R_2 = 3*sigma_R_2

time_P_2 = np.array(settling_times_P_2[-1])
data_P_2 = Pitch_2[int(time_P_2[0]/2):int(time_P_2[1]/2)]
# Calcular media y desviación estándar
media_P_2 = np.mean(data_P_2)
sigma_P_2 = np.std(data_P_2)
# Calcular los límites de 3 sigma
lim_inf_P_2 = media_P_2 - 3 * sigma_P_2
lim_sup_P_2 = media_P_2 + 3 * sigma_P_2
accuracy_P_2 = 3*sigma_P_2

time_Y_2 = np.array(settling_times_Y_2[-1])
data_Y_2= Yaw_2[int(time_Y_2[0]/2):int(time_Y_2[1]/2)]
# Calcular media y desviación estándar
media_Y_2 = np.mean(data_Y_2)
sigma_Y_2 = np.std(data_Y_2)
# Calcular los límites de 3 sigma
lim_inf_Y_2 = media_Y_2 - 3 * sigma_Y_2
lim_sup_Y_2 = media_Y_2 + 3 * sigma_Y_2
accuracy_Y_2 = 3*sigma_Y_2

accuracy_RPY_2 = np.array([accuracy_R_2,accuracy_P_2,accuracy_Y_2])
# print("La exactitud de apuntamiento para Roll, Pitch y Yaw son respecticamente: \n", accuracy_RPY_2, "[°]")


time_R_3 = np.array(settling_times_R_3[-1])
data_R_3 = Roll_3[int(time_R_3[0]/2):int(time_R_3[1]/2)]
# Calcular media y desviación estándar
media_R_3 = np.mean(data_R_3)
sigma_R_3 = np.std(data_R_3)
# Calcular los límites de 3 sigma
lim_inf_R_3 = media_R_3 - 3 * sigma_R_3
lim_sup_R_3 = media_R_3 + 3 * sigma_R_3
accuracy_R_3 = 3*sigma_R_3

time_P_3 = np.array(settling_times_P_3[-1])
data_P_3 = Pitch_3[int(time_P_3[0]/2):int(time_P_3[1]/2)]
# Calcular media y desviación estándar
media_P_3 = np.mean(data_P_3)
sigma_P_3 = np.std(data_P_3)
# Calcular los límites de 3 sigma
lim_inf_P_3 = media_P_3 - 3 * sigma_P_3
lim_sup_P_3 = media_P_3 + 3 * sigma_P_3
accuracy_P_3 = 3*sigma_P_3

time_Y_3 = np.array(settling_times_Y_3[-1])
data_Y_3= Yaw_3[int(time_Y_3[0]/2):int(time_Y_3[1]/2)]
# Calcular media y desviación estándar
media_Y_3 = np.mean(data_Y_3)
sigma_Y_3 = np.std(data_Y_3)
# Calcular los límites de 3 sigma
lim_inf_Y_3 = media_Y_3 - 3 * sigma_Y_3
lim_sup_Y_3 = media_Y_3 + 3 * sigma_Y_3
accuracy_Y_3 = 3*sigma_Y_3

accuracy_RPY_3 = np.array([accuracy_R_3,accuracy_P_3,accuracy_Y_3])
# print("La exactitud de apuntamiento para Roll, Pitch y Yaw son respecticamente: \n", accuracy_RPY_3, "[°]")

#%%

# normas de densidad espectro potencia
norm_psd_RPY_1 = np.linalg.norm(psd_RPY_1)
norm_psd_RPY_2 = np.linalg.norm(psd_RPY_2)
norm_psd_RPY_3 = np.linalg.norm(psd_RPY_3)

# normas de tiempo de asentamiento
norm_settling_time_1 = np.linalg.norm(np.array([time_R_1[0],time_P_1[0],time_Y_1[0]]))
norm_settling_time_2 = np.linalg.norm(np.array([time_R_2[0],time_P_2[0],time_Y_2[0]]))
norm_settling_time_3 = np.linalg.norm(np.array([time_R_3[0],time_P_3[0],time_Y_3[0]]))

# normas de exactitud de apuntamiento
norm_accuracy_1 = np.linalg.norm(accuracy_RPY_1)
norm_accuracy_2 = np.linalg.norm(accuracy_RPY_2)
norm_accuracy_3 = np.linalg.norm(accuracy_RPY_3)

# Crear el DataFrame
resumen_1 = {
    "Opción": archivos_seleccionados,
    "PSD Roll [W/Hz]": [psd_RPY_1[0], psd_RPY_2[0], psd_RPY_3[0]],
    "PSD Pitch [W/Hz]": [psd_RPY_1[1], psd_RPY_2[1], psd_RPY_3][1],
    "PSD Yaw [W/Hz]": [psd_RPY_1[2], psd_RPY_2[2], psd_RPY_3[2]],

    "Agilidad Roll [s]": [time_R_1[0], time_R_2[0], time_R_3[0]],
    "Agilidad Pitch [s]": [time_P_1[0], time_P_2[0], time_P_3[0]],
    "Agilidad Yaw[s]": [time_Y_1[0], time_Y_2[0], time_Y_3[0]],

    "Exactitud Roll [°]": [accuracy_RPY_1[0], accuracy_RPY_2[0], accuracy_RPY_3[0]],
    "Exactitud Pitch [°]": [accuracy_RPY_1[1], accuracy_RPY_3[1], accuracy_RPY_3[1]],
    "Exactitud Yaw [°]": [accuracy_RPY_1[2], accuracy_RPY_3[2], accuracy_RPY_3[2]],

}

resumen_2 = {
    "Opción": archivos_seleccionados,
    "Norma PSD [W/Hz]": [norm_psd_RPY_1, norm_psd_RPY_2, norm_psd_RPY_3],
    "Norma Agilidad [s]": [norm_settling_time_1, norm_settling_time_2, norm_settling_time_3],
    "Norma Exactitud [°]": [norm_accuracy_1, norm_accuracy_2, norm_accuracy_3]
}

tabla_1 = pd.DataFrame(resumen_1)
tabla_1_transposed = tabla_1.set_index("Opción").transpose()

tabla_2 = pd.DataFrame(resumen_2)
tabla_2_transposed = tabla_2.set_index("Opción").transpose()

# Imprimir la tabla
print("\n")
print(tabla_1_transposed)
print("\n")
print(tabla_2_transposed)

nombre_archivo_1 = os.path.splitext(os.path.basename(archivos_seleccionados[0]))[0]
nombre_archivo_2 = os.path.splitext(os.path.basename(archivos_seleccionados[1]))[0]
nombre_archivo_3 = os.path.splitext(os.path.basename(archivos_seleccionados[2]))[0]

#%%

fig0, axes0 = plt.subplots(nrows=3, ncols=1, figsize=(13, 8))

axes0[0].plot(t_aux, Roll_1, label= {nombre_archivo_1})
axes0[0].plot(t_aux, Roll_2, label= {nombre_archivo_2})
axes0[0].plot(t_aux, Roll_3, label= {nombre_archivo_3})
axes0[0].set_xlabel('Tiempo [s]')
axes0[0].set_ylabel('Roll [°]')
axes0[0].legend()
axes0[0].grid()
#axes0[0].set_ylim(-1, 1)  # Ajusta los límites en el eje Y

axes0[1].plot(t_aux, Pitch_1, label={nombre_archivo_1})
axes0[1].plot(t_aux, Pitch_2, label={nombre_archivo_2})
axes0[1].plot(t_aux, Pitch_3, label={nombre_archivo_3})
axes0[1].set_xlabel('Tiempo [s]')
axes0[1].set_ylabel('Pitch [°]')
axes0[1].legend()
axes0[1].grid()
# axes0[1].set_ylim(-20, -5)  # Ajusta los límites en el eje Y
# axes0[1].set_xlim(150000, 400000)  # Ajusta los límites en el eje Y

axes0[2].plot(t_aux, Yaw_1, label={nombre_archivo_1})
axes0[2].plot(t_aux, Yaw_2, label={nombre_archivo_2})
axes0[2].plot(t_aux, Yaw_3, label={nombre_archivo_3})
axes0[2].set_xlabel('Tiempo [s]')
axes0[2].set_ylabel('Yaw [°]')
axes0[2].legend()
axes0[2].grid()
# axes0[2].set_ylim(-20, -5)  # Ajusta los límites en el eje Y
# axes0[2].set_xlim(150000, 400000)  # Ajusta los límites en el eje Y

plt.tight_layout()
plt.show()