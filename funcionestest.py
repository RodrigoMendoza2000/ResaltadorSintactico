import pandas as pd

import math

players = pd.read_csv('Players1.csv', delimiter = ',', decimal = ".", header = 0, index_col = 0)

print(players.head())

"""def funcion(dataframe, column):
  diccionario = {"Media":players["minutes"].mean(),
  "Mediana":players["minutes"].median(),"Min":players["minutes"].min(),
  "Max":players["minutes"].max()}
  return diccionario

funcion(players, "minutes")"""


def function(dataframe, columna1, columna2):
  correlacion = np.corrcoef(dataframe.iloc[:, columna1], dataframe.iloc[:, columna2])
  return correlacion

print(function(players, 3, 4))

r = abs((4**3 - math.factorial(3))*(13/12))
print(r)

x = [15,34,72,23,91,4,201,68,56,78]
print(type(x))

y = x.reverse()
print(hola)