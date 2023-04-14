# Importando librerías
import pandas as pd
import numpy as np
import yfinance as yf
import quandl

# Dirección de la API de quandl

QUANDL_API_KEY = '{API KEY}'
quandl.ApiConfig.api_key = QUANDL_API_KEY

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

""" 
Creando un DataFrame con la unión de las fechas (a la izquierda) y los precios de cierre a la derecha
Se usa combinación izquierda que devuelve todas las filas de la tabla izquierda y las filas coincidentes
de la tabla derecha mientras deja vacías las filas no coincidentes

"""

df_all_dates = pd.DataFrame(index=pd.date_range(start = '2009-12-31',
                                                end = '2020-11-30'))
df = df_all_dates.join(df[['adj_close']], how='left')\
                 .fillna(method='ffill')\
                 .asfreq('M') 

# Descarga de datos de inflación de Quandl:
df_cpi = quandl.get(dataset='RATEINF/CPI_USA',
                    start_date = '2009-12-01',
                    end_date = '2020-11-30')
df_cpi.rename(columns={'Value':'cpi'}, inplace=True)

# Combinar los datos de inflación con los precios

df_merged = df.join(df_cpi, how='left')

#Calculo de rendimientos simples y tasa de inflación

df_merged['simple_rtn'] = df_merged.adj_close.pct_change()
df_merged['inflation_rate'] = df_merged.cpi.pct_change()

# Ajuste de rendimientos por inflación

df_merged['real_rtn'] = (df_merged.simple_rtn +1) / (df_merged.inflation_rate + 1) - 1

#Mostrando los datos

print(df_merged)

