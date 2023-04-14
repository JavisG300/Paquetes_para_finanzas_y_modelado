#Importar librerias

import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt
import warnings

#Descarga de datos para mantener solo precios de cierre ajustados

df = yf.download('MSFT',
                 start='1988-01-01',
                 end='2023-12-31',
                 progress=False)

df = df.loc[:, ['Adj Close']]
df.rename(columns={'Adj Close': 'adj_close'}, inplace=True)

#Calcular los rendimientos simples y logaritmicos

df['simple_rtn'] = df.adj_close.pct_change() #Rendimientos simples
df['log_rtn'] = np.log(df.adj_close/df.adj_close.shift(1)) #Rendimientos logaritmicos

#Estableciendo la figura
fig, ax= plt.subplots(3, 1, figsize=(12, 10), sharex=True)

#Agregando precios

df.adj_close.plot(ax=ax[0])
ax[0].set(title = 'MSFT time series',
          ylabel = 'Stock price ($)')

#Agregando rendimientos simples

df.simple_rtn.plot(ax=ax[1])
ax[1].set(ylabel = 'Simple returns (%)')

#Agregarndo rendimientos logaritmicos

df.log_rtn.plot(ax=ax[2])
ax[2].set(xlabel = 'Date',
          ylabel = 'Log returns (%)')
ax[2].tick_params(axis='x',
                  which = 'major',
                  labelsize=12)
#Guardando y mostrando grafico
plt.savefig('Visualizacion_series_de_tiempo.png')
plt.show()

