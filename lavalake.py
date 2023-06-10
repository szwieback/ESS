'''
Created on May 22, 2023

@author: simon
'''
import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
params_def = {'A': 1, 'Q': 1.0, 'alpha': 0.1, 'beta': 0.6, 'gamma': 1, 'P_crit': 5}

def f_lake(t, y, params=params_def):
    # y: h, C
    Q, A = params['Q'], params['A']
    C = y[1]
    dydt = np.zeros(2)
    P = params['gamma'] * y[0]
        
    flux = P * C
    dydt[0] = Q/A - flux
    # dydt[1] = params['alpha'] * params['A'] *  flux  - params['beta'] *  y[1]
    dP_crit = 0 if P < params['P_crit'] else P - params['P_crit']
    if P < params['P_crit']:
        dydt[1] = -params['beta'] * y[1]
    else:
        dydt[1] = params['alpha'] * y[1]
    # dydt[1] = -params['beta'] * y[1] + 1.0 * dP_crit
    return dydt


t_eval = np.arange(0, 100, 0.05)
y0 = [0.0, 0.1]
_f_lake = f_lake
sol = solve_ivp(_f_lake, [t_eval[0], t_eval[-1]], y0, t_eval=t_eval)
fig, axs = plt.subplots(nrows=2)
axs[0].plot(t_eval, sol.y[0, :])
axs[1].plot(t_eval, sol.y[1, :])
plt.show()
