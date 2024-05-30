# -*- coding: utf-8 -*-
"""
Created on Tue Apr 30 15:13:44 2024

@author: nachi
"""
import functions_03
import numpy as np
import control as ctrl
import pandas as pd
import matplotlib.pyplot as plt
from scipy.spatial.transform import Rotation
from sklearn.decomposition import PCA

# %%
archivo_csv = "Vectores_orbit_ECI.csv"

# Leer el archivo CSV en un DataFrame de pandas
df = pd.read_csv(archivo_csv)

# Convertir el DataFrame a un array de NumPy
array_datos = df.to_numpy()

t_aux = array_datos[:, 0]
Bx_orbit = array_datos[:, 1]
By_orbit = array_datos[:, 2]
Bz_orbit = array_datos[:, 3]
Bx_IGRF = array_datos[:, 4]
By_IGRF = array_datos[:, 5]
Bz_IGRF = array_datos[:, 6]
vx_sun_orbit = array_datos[:, 7]
vy_sun_orbit = array_datos[:, 8]
vz_sun_orbit = array_datos[:, 9]
vsun_x = array_datos[:, 10]
vsun_y = array_datos[:, 11]
vsun_z = array_datos[:, 12]
#%%
w0_O = 0.00163

deltat = 2
limite =  5762*2
t = np.arange(0, limite, deltat)

I_x = 0.037
I_y = 0.036
I_z = 0.006

w0_eq = 0
w1_eq = 0
w2_eq = 0

sigma_ss = 0.036
sigma_b = 1e-6

#%%
# q= np.array([0,0.7071,0,0.7071])
# q= np.array([0,0,0,1])
q = np.array([0.7071/np.sqrt(3),0.7071/np.sqrt(3),0.7071/np.sqrt(3),0.7071])
w = np.array([0.0001, 0.0001, 0.0001])
# q_est = np.array([0.00985969, 0.70703804, 0.00985969, 0.70703804])
# q_est= np.array([0.0120039,0.0116517,0.0160542,0.999731])
q_est = np.array([0.366144,0.464586,0.300017,0.74839])

q0_est = [q_est[0]]
q1_est = [q_est[1]]
q2_est = [q_est[2]]
q3_est = [q_est[3]]
w0_est = [w[0]]
w1_est = [w[1]]
w2_est = [w[2]]
# x_est = np.hstack((q_est[0:3],w))

q0_real = [q[0]]
q1_real = [q[1]]
q2_real = [q[2]]
q3_real = [q[3]]
w0_real = [w[0]]
w1_real = [w[1]]
w2_real = [w[2]]
q_real = np.array([q0_real[-1],q1_real[-1],q2_real[-1],q3_real[-1]])
w_body = np.array([w0_real[-1], w1_real[-1], w2_real[-1]])
w_gyros = functions_03.simulate_gyros_reading(w_body, 0,0)
x_real = np.hstack((np.transpose(q_real[:3]), np.transpose(w_gyros)))

bi_orbit = [Bx_orbit[0],By_orbit[0],Bz_orbit[0]]
b_body_i = functions_03.rotacion_v(q_real, bi_orbit, 1e-6)

si_orbit = [vx_sun_orbit[0],vy_sun_orbit[0],vz_sun_orbit[0]]
s_body_i = functions_03.rotacion_v(q_real, si_orbit, 0.036)
hh =0.01

[A,B,C,A_discrete,B_discrete,C_discrete] = functions_03.A_B(I_x, I_y, I_z, w0_O, w0_eq, w1_eq, w2_eq, deltat, hh, bi_orbit,b_body_i, s_body_i)

B_matrices = [B_discrete]
#%%
# for i in range(len(t[0:2882])-1):
for i in range(len(t)-1):

    print(t[i+1])
    
    # u_est = np.array([15,15,15])

    b_orbit = [Bx_orbit[i+1],By_orbit[i+1],Bz_orbit[i+1]]

    [A,B,C,A_discrete,B_discrete,C_discrete] = functions_03.A_B(I_x, I_y, I_z, w0_O, w0_eq, w1_eq, w2_eq, deltat, hh,b_orbit, np.zeros(3), np.zeros(3))

    B_matrices.append(B_discrete)

# Aplana y apila todas las matrices en una sola matriz grande
data = np.array([matrix.flatten() for matrix in B_matrices])

# Crear una instancia del PCA
n_components = 1  # Queremos una representación compacta, así que usamos 1 componente principal
pca = PCA(n_components=n_components)

# Ajustar el PCA a los datos y transformarlos
transformed_data = pca.fit_transform(data)

# Para obtener una representación compacta, calculamos la media de las transformaciones
mean_transformed = np.mean(transformed_data, axis=0)

# Inversa la transformación de PCA para volver al espacio original (18 dimensiones)
mean_transformed_back = pca.inverse_transform(mean_transformed)

# Reshape el vector resultante de 18 elementos a una matriz de 6x3
B_prom = mean_transformed_back.reshape(6, 3)
x0 = np.array([ -100 ,   200, -300,  -200,
  -400, -100])

optimal_x = functions_03.opt_K(A_discrete, B_prom, deltat, hh, x0)
K = np.hstack([np.diag(optimal_x[:3]), np.diag(optimal_x[3:])])


# optimal_x = functions_03.opt_K(A_discrete, B_discrete, deltat, hh, x0)
# diag_K = np.array([ -241.00245091,    43.60100138, -3058.43592597,  -559.64142154,
#   -154.34336893, -5160.75960109])
# K = np.hstack([np.diag(optimal_x[:3]), np.diag(optimal_x[3:])])
# x0 = optimal_x
diagonal_values = np.array([0.5**2, 0.5**2, 0.5**2, 0.1**2, 0.1**2, 0.1**2])
P_ki = np.diag(diagonal_values)

#%%
np.random.seed(42)
for i in range(len(t)-1):
    print(t[i+1])
    q_est = np.array([q0_est[-1], q1_est[-1], q2_est[-1], q3_est[-1]])
    w_est = np.array([w0_est[-1], w1_est[-1], w2_est[-1]])
    x_est = np.hstack((np.transpose(q_est[:3]), np.transpose(w_est)))
    # u_est = np.array([15,15,15])
    u_est = np.dot(K,x_est)

    x_est = np.hstack((q_est[0:3],w_est))  

    b_orbit = [Bx_orbit[i+1],By_orbit[i+1],Bz_orbit[i+1]]
    b_body = functions_03.rotacion_v(q_real, b_orbit, sigma_b)

    vsun_orbit = [vx_sun_orbit[i+1],vy_sun_orbit[i+1],vz_sun_orbit[i+1]]
    s_body = functions_03.rotacion_v(q_real, vsun_orbit, sigma_ss)

    print(x_est)
    print(q_real)
    print(w_gyros)
    
    # print(b_body,w_gyros)
    # print(x_est)
    [A,B,C,A_discrete,B_discrete,C_discrete] = functions_03.A_B(I_x, I_y, I_z, w0_O, w0_eq, w1_eq, w2_eq, deltat, hh, b_orbit,b_body, s_body)
    [q_posteriori, w_posteriori, P_k_pos,K_k] = functions_03.kalman_lineal(A_discrete, B_prom,C_discrete, x_real, u_est, b_body, s_body, P_ki, sigma_b, sigma_ss, deltat,hh)
    # asasd
    
    q0_est.append(q_posteriori[0])
    q1_est.append(q_posteriori[1])
    q2_est.append(q_posteriori[2])
    q3_est.append(q_posteriori[3])
    w0_est.append(w_posteriori[0])
    w1_est.append(w_posteriori[1])
    w2_est.append(w_posteriori[2])

    P_ki = P_k_pos
    
    [xx_new_d, qq3_new_d] = functions_03.mod_lineal_disc(
        x_real, u_est, deltat, hh, A_discrete,B_prom)
    
    x_real = xx_new_d

    q0_real.append(xx_new_d[0])
    q1_real.append(xx_new_d[1])
    q2_real.append(xx_new_d[2])
    q3_real.append(qq3_new_d)
    w0_real.append(xx_new_d[3])
    w1_real.append(xx_new_d[4])
    w2_real.append(xx_new_d[5])

    q_real = np.array([q0_real[-1], q1_real[-1], q2_real[-1], q3_real[-1]])
    w_real = np.array([w0_real[-1], w1_real[-1], w2_real[-1]])
    w_gyros = functions_03.simulate_gyros_reading(w_real, 0,0)

[MSE_cuat, MSE_omega]  = functions_03.cuat_MSE_NL(q0_real, q1_real, q2_real, q3_real, w0_real, w1_real, w2_real, q0_est, q1_est, q2_est, q3_est, w0_est, w1_est, w2_est)   
[RPY_all_est,RPY_all_id,mse_roll,mse_pitch,mse_yaw] = functions_03.RPY_MSE(t, q0_est, q1_est, q2_est, q3_est, q0_real, q1_real, q2_real, q3_real)   
    
# %%
fig0, axes0 = plt.subplots(nrows=1, ncols=2, figsize=(16, 4))

axes0[0].plot(t, q0_real, label='q0 modelo')
axes0[0].plot(t, q1_real, label='q1 modelo')
axes0[0].plot(t, q2_real, label='q2 modelo')
axes0[0].plot(t, q3_real, label='q3 modelo')
axes0[0].set_xlabel('Tiempo [s]')
axes0[0].set_ylabel('cuaternion [-]')
axes0[0].legend()
axes0[0].set_title('cuaterniones obtenidos por el modelo de control lineal discreto')
axes0[0].grid()
# axes0[0].set_ylim(-1, 1)  # Ajusta los límites en el eje Y

axes0[1].plot(t, q0_est, label='q0 kalman')
axes0[1].plot(t, q1_est, label='q1 kalman')
axes0[1].plot(t, q2_est, label='q2 kalman')
axes0[1].plot(t, q3_est, label='q3 kalman')
axes0[1].set_xlabel('Tiempo [s]')
axes0[1].set_ylabel('cuaternion [-]')
axes0[1].legend()
axes0[1].set_title('cuaterniones estimados por el filtro de kalman lineal discreto')
axes0[1].grid()
plt.tight_layout()
plt.show()

fig0, axes0 = plt.subplots(nrows=1, ncols=2, figsize=(16, 4))

axes0[0].plot(t, w0_real, label='w0 modelo')
axes0[0].plot(t, w1_real, label='w1 modelo')
axes0[0].plot(t, w2_real, label='w2 modelo')
axes0[0].set_xlabel('Tiempo [s]')
axes0[0].set_ylabel('velocidad angular [rad/s]')
axes0[0].legend()
axes0[0].set_title('velocidades angulares obtenidos por el modelo de control lineal discreto')
axes0[0].grid()
# axes0[0].set_ylim(-1, 1)  # Ajusta los límites en el eje Y

axes0[1].plot(t, w0_est, label='w0 kalman')
axes0[1].plot(t, w1_est, label='w1 kalman')
axes0[1].plot(t, w2_est, label='w2 kalman')
axes0[1].set_xlabel('Tiempo [s]')
axes0[1].set_ylabel('velocidad angular [rad/s]')
axes0[1].legend()
axes0[1].set_title('velocidades angulares estimados por el filtro de kalman lineal discreto')
axes0[1].grid()
plt.tight_layout()
plt.show()

quats = np.array([0,1,2,3])
plt.figure(figsize=(12, 6))
plt.scatter(quats[0], MSE_cuat[0], label='mse q0', color='r',marker='*')
plt.scatter(quats[1], MSE_cuat[1], label='mse q1', color='b',marker='*')
plt.scatter(quats[2], MSE_cuat[2], label='mse q2', color='k',marker='*')
plt.scatter(quats[3], MSE_cuat[3], label='mse q3', color='g',marker='*')
plt.xlabel('Cuaterniones')
plt.ylabel('Mean Square Error [-]')
plt.legend()
plt.title('MSE de cada cuaternion entre lineal discreto y kalman lineal discreto')
# plt.xlim(20000,100000)
# plt.ylim(-0.005,0.005)
plt.grid()
plt.show()

vels = np.array([0,1,2])
plt.figure(figsize=(12, 6))
plt.scatter(vels[0], MSE_omega[0], label='mse w0', color='r',marker='*')
plt.scatter(vels[1], MSE_omega[1], label='mse w1', color='b',marker='*')
plt.scatter(vels[2], MSE_omega[2], label='mse w2', color='k',marker='*')
plt.xlabel('Velocidades angulares')
plt.ylabel('Mean Square Error [rad/s]')
plt.legend()
plt.title('MSE de cada velocidad angular entre lineal discreto y kalman lineal discreto')
# plt.xlim(20000,100000)
# plt.ylim(-0.005,0.005)
plt.grid()
plt.show()

fig0, axes0 = plt.subplots(nrows=1, ncols=2, figsize=(16, 4))

axes0[0].plot(t, RPY_all_id[:,0], label='Roll modelo')
axes0[0].plot(t, RPY_all_id[:,1], label='Pitch modelo')
axes0[0].plot(t, RPY_all_id[:,2], label='Yaw modelo')
axes0[0].set_xlabel('Tiempo [s]')
axes0[0].set_ylabel('Angulos de Euler [°]')
axes0[0].legend()
axes0[0].set_title('Angulos de Euler obtenidos por el modelo de control lineal discreto')
axes0[0].grid()
# axes0[0].set_ylim(-1, 1)  # Ajusta los límites en el eje Y

axes0[1].plot(t, RPY_all_est[:,0], label='Roll kalman')
axes0[1].plot(t, RPY_all_est[:,1], label='Pitch kalman')
axes0[1].plot(t, RPY_all_est[:,2], label='Yaw kalman')
axes0[1].set_xlabel('Tiempo [s]')
axes0[1].set_ylabel('Angulos de Euler [°]')
axes0[1].legend()
axes0[1].set_title('Angulos de Euler estimados por el filtro de kalman lineal discreto')
axes0[1].grid()
plt.tight_layout()
plt.show()

# R_P_Y = np.array([0,1,2])
# plt.figure(figsize=(12, 6))
# plt.scatter(R_P_Y [0], mse_roll, label='mse roll', color='r',marker='*')
# plt.scatter(R_P_Y [1], mse_pitch, label='mse pitch', color='b',marker='*')
# plt.scatter(R_P_Y [2], mse_yaw, label='mse yaw', color='k',marker='*')
# plt.xlabel('Angulos de Euler')
# plt.ylabel('Mean Square Error [°]')
# plt.legend()
# plt.title('MSE de cada angulo de Euler entre lineal discreto y kalman lineal discreto')
# # plt.xlim(20000,100000)
# # plt.ylim(-0.005,0.005)
# plt.grid()
# plt.show()