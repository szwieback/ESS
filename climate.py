'''
Created on May 23, 2023

@author: simon
'''
import numpy as np
from scipy.constants import Stefan_Boltzmann as sigma
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
from collections.abc import Iterable
year = (60 * 60 * 24 * 365.25)

C = 4e8  # per unit area
albedo_snow = 0.75
albedo_nosnow = 0.25
T_half = 260
T_range = 15#10
emiss = 0.65
S0 = 342  # accounts for night; per unit area

def albedo(T):
    frac = 0.5 * (1 + np.tanh((T - T_half) / (T_range)))
    return (albedo_nosnow - albedo_snow) * frac + albedo_snow

def S_in(T):
    return S0 * (1 - albedo(T))

def S_out(T, emiss=emiss):
    return emiss * sigma * T ** 4

def net_forcing(T, emiss=emiss):
    return S_in(T) - S_out(T, emiss=emiss)

def _dTdt(t, T):
    return net_forcing(T) / C

T_grid = np.linspace(150, 350, num=201)
# plt.plot(T_grid, albedo(T_grid))
# plt.show()

t_eval = np.linspace(0, 100 * year, num=1000)
T0 = [270]  # [270]
sol = solve_ivp(_dTdt, [t_eval[0], t_eval[-1]], T0, t_eval=t_eval, method='LSODA')
T = sol.y[0,:]
# plt.plot(t_eval, T)
# plt.show()

S_in_grid = S_in(T_grid)
S_out_grid = S_out(T_grid)
# plt.plot(T_grid, S_in_grid, label='S_in')
# plt.plot(T_grid, S_out_grid, label='S_out')
# plt.show()

net_grid = net_forcing(T_grid)

def stationary_points(T_grid, emiss=emiss):
    def _stationary_points_single(_emiss):
        net_grid = net_forcing(T_grid, emiss=_emiss)
        sign_changes = np.signbit(net_grid[1:] * net_grid[:-1])
        s_stat = (np.signbit(net_grid)[1:][sign_changes]) #stable
        T_stat = 0.5 * (T_grid[1:][sign_changes] + T_grid[:-1][sign_changes])
        return T_stat, s_stat
    return [_stationary_points_single(em) for em in np.atleast_1d(emiss)]

# print(stationary_points(T_grid))

emiss_grid = np.linspace(0.3, 1.0, num=64)
stat = stationary_points(T_grid, emiss=emiss_grid)
cols= {True: '#333366', False: '#cc9999'}
for _emiss, _stat in zip(emiss_grid, stat):
    for _T, _s in zip(*_stat):
        plt.plot(_emiss, _T, linestyle='none', marker='o', ms=1, c=cols[_s])
plt.show()

