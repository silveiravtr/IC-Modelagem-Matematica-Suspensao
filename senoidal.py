# -*- coding: utf-8 -*-
"""Senoidal.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1mzWcEmlF8Fh20vR0GeEAAFi4t0B4V0jW
"""

#Importando bibliotecas
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

#Parâmetros do sistema
m1 = 6.0       #Massa não suspensa [kg]
m2 = 58.5      #Massa suspensa [kg]
k1 = 39500.0   #Rigidez do pneu [N/m]
k2 = 3950.0    #Rigidez da mola da suspensão [N/m]

#Coeficientes de amortecimento
zeta = [0.7, 1.0, 1.4]
b = [2 * z * np.sqrt(k2 * m2) for z in zeta]

#Configuração da simulação
f0 = 2.0  #Frequência de excitação em Hz
omega0 = 2 * np.pi * f0
t_span = (0, 5)  #Tempo inicial e final [s]
t_eval = np.linspace(0, 5, 5000)  #Vetor temporal

#Função de entrada senoidal
def u_senoidal(t):
    return np.sin(omega0 * t)

#Sistema dinâmico de ¼ de suspensão
def sistema_senoidal(t, Y, m1, m2, b, k1, k2):
    x, dx, y, dy = Y  #Descompacta os estados

    #Cálculo completo das acelerações em uma única linha
    ddx = (-b*(dx - dy) - k2*(x - y) - k1*(x - u_senoidal(t))) / m1
    ddy = (-b*(dy - dx) - k2*(y - x)) / m2

    return [dx, ddx, dy, ddy]

#Simulação para cada valor de amortecimento
for i, bi in enumerate(b):
    #Resolve o sistema de EDOs
    sol = solve_ivp(sistema_senoidal, t_span, [0, 0, 0, 0],
                    args=(m1, m2, bi, k1, k2),
                    t_eval=t_eval,
                    method='RK45',
                    rtol=1e-6,
                    atol=1e-8)

    #Extrai os resultados
    x = sol.y[0]  #Posição da massa não suspensa
    y = sol.y[2]  #Posição da massa suspensa

    #Plot dos resultados
    plt.figure(figsize=(12, 5))
    plt.plot(t_eval, u_senoidal(t_eval), ':', label='Entrada senoidal', alpha=0.7)
    plt.plot(t_eval, x, label='x(t) - Massa não suspensa')
    plt.plot(t_eval, y, '--', label='y(t) - Massa suspensa')

    plt.title(f'Resposta à Excitação Senoidal (2 Hz) para ζ = {zeta[i]}')
    plt.xlabel('Tempo [s]')
    plt.ylabel('Deslocamento [m]')
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()