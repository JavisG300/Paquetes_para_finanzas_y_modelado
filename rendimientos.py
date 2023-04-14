# Importando librerías
import pandas as pd
import numpy as np
import yfinance as yf

# Descarga de datos (únicamente precios de cierre)

df = yf.download('AAPL',
                 start='2010-01-01',
                 end='2020-11-30',
                 progress=False)
df = df.loc[:, ['Adj Close']]
df.rename(columns={'Adj Close': 'adj_close'}, inplace=True)

# Calculando rendimientos simples y log utilizando precios de cierre ajustados

df['simple_rtn'] = df.adj_close.pct_change() #Rendimientos simples
df['log_rtn'] = np.log(df.adj_close/df.adj_close.shift(1)) #Rendimientos logaritmicos

# Mostrando resultados

print(df)