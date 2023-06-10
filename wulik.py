'''
Created on Jun 5, 2023

@author: simon
'''
import os
import pandas as pd
import datetime as dt
path0 = '/home/simon/Work/IESS/'
fnmet = os.path.join(path0, 'kivalina.csv')
fnsf = os.path.join(path0, 'wulik.tsv')
fnwulik = os.path.join(path0, 'wulik_2021.csv')
def read_weather(fnmet):
    pass

def read_streamflow(fnsf, fnout):
    #area: 2340 km2 vers. 705 sqm
    df = pd.read_csv(fnsf, skiprows=31, sep='\t', names=['t', 'g', 'dt', 'tz', 'Q', 'qc'])
    df = df.drop(columns=['t', 'g'])
    df['Q'] = df['Q'].astype('float') * 0.02832 # m3/s
    df = df.set_index(pd.to_datetime(df['dt']))
    dfQ = df['Q'].resample('D').mean() * (60 * 60 * 24) #m3/day
    import matplotlib.pyplot as plt
    plt.plot(dfQ.index, dfQ)
    plt.show()
    dfQ_y = dfQ.loc['2020-11-1':'2021-10-30']
    dfQ_y.to_csv(fnout)
    
if __name__ == '__main__':
    read_streamflow(fnsf, fnwulik)
    