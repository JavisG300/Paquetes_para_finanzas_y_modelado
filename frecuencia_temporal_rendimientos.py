#Importar librerias requeridas

#matplotlib inline
#congif InlineBackend.figure_format = 'retina'

import pandas as pd
import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt
import warnings

#Definir estilo del gráfico y control mensajes de advertencia

plt.style.use('seaborn')
#plt.style.use(0seaborn-colorblind) #Alternativa
#plt.rcParams['figure.dpi']=[16, 9]
plt.rcParams['figure.dpi'] = 300
warnings.simplefilter(action='ignore', category=FutureWarning)

#Descarga de datos
df = yf.download('AAPL',
                 start = '2010-01-01',
                 end = '2020-11-30',
                 auto_adjust=False,
                 progress=False)

#Guardar solamente el precio de cierre ajustado

df = df.loc[:, ['Adj Close']]
df.rename(columns = {'Adj Close': 'adj_close'}, inplace = True)

#Calcular los rendimientos
df['log_rtn'] = np.log(df.adj_close/df.adj_close.shift(1))

#Eliminar datos redundantes
df.drop('adj_close', axis=1, inplace=True)
df.dropna(axis=0, inplace=True)

#Definir la función para calcular la volatilidad histórica
def realized_volatility(x):
    return np.sqrt(np.sum(x**2))

#Calcular la volatilidad hitórica mensual
df_rv = df.groupby(pd.Grouper(freq='M')).apply(realized_volatility)
df_rv.rename(columns={'log_rtn':'rv'}, inplace=True)

#Anualizar los valores
df_rv.rv = df_rv.rv * np.sqrt(12)

#Graficar los resultados
fig, ax = plt.subplots(2, 1, sharex = True)
ax[0].plot(df)
ax[1].plot(df_rv)
plt.show()