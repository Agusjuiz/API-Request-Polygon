# -*- coding: utf-8 -*-
"""
Created on Thu Oct 13 12:04:49 2022

@author: agusj
"""

import requests
from datetime import datetime as dt_dt
import pandas as pd
import sqlite3
import mplfinance as mpf
    

 
#-------------------------------------------------------------------------------------
# DEFINICION DE FUNCIONES
#-------------------------------------------------------------------------------------   
# Creamos la función integ_Input para convertir en enteros los valores ingresados por el usuario
# y asi evitar errores en la función input_Rango, dado que esta última trabaja con operadores
# de comparación los cuales son compatibles con nros.
    
def integ_Input(texto):
    val = 0
    while True:
        try:
            # convierte en integer
            inp = input(texto)
            val = int(inp)
            break
        except ValueError:
            print("Valor erroneo. Intentelo nuevamente.")
    return val

#Creamos una función en la cual se define la variable rango de forma tal que el usuario puedan ingresar
# números del 1 al 7 que sean coincidentes con el timespan de la API.

def input_Rango():
    flag = False
    rg = ""
    while flag == False:
        print('Debe definir un espacio de tiempo: \n 1) minuto \n 2) hora \n 3) dia \n 4) semanal \n 5) mensual \n 6) trimestral \n 7) anual')
        num = integ_Input("Defina un intervalo de tiempo: ")
        
        
        if num > 0 and num <= 7:
            flag = True
            
            if num == 1:
                rg = "minute"
               
            elif num == 2:
                rg = "hour"
            
            elif num == 3:
                rg = "day"
                
            elif num == 4:
                rg = "week"
                
            elif num == 5:
                rg = "month"
                
            elif num == 6:
                rg = "quarter"
                
            elif num == 7:
                rg = "year"
        else:
            print("\n\n El intervalo seleccionado es incorrecto. Vuelva a ingresarlo nuevamente: ")
    return rg            
                

#La función input_Multiplicador, fue pensada para que el usuario pueda ingresar el multiplicador de rango de tiempo
# que trae la API (EJ: 1 min, 5 min, 2 hs, etc.) pero limitando errores dados que la API permite números negativos.
# Finalmente la función convierte el resultado en STR para que la URL de la API lo tome correctamente.
                
def input_Multiplicador(param_rango):
    flag = False
    mt = 0
    while flag == False:
        if rango == "minute":
            num = integ_Input("Puede visualizar barras de entre 1 y 59 minutos: ")
            if num > 0 and num <= 59:
                flag = True
                mt = num
            else:
                print("\n\n El intervalo de tiempo es incorrecto. Intentelo nuevamente: " )
        elif rango == "hour":
            num = integ_Input("Puede visualizar barras de entre 1 y 23 horas: ")
            if num > 0 and num <= 23:
                flag = True
                mt = num
            else:
                print("\n\n El intervalo de tiempo es incorrecto. Intentelo nuevamente: " )
        else:
            mt = 1
            flag = True
    return str(mt)

#La función format_Fechas convierte las fechas de string a date para poder validar el formato que ingresa el usuario. 
#Dejamos que igualmente la API tome la variable str.

def format_Fechas(texto):
    datetime_to_date = 0
      
    while True:
        try:
            fecha_inp = input(texto)
            fecha_inp_conv = dt_dt.strptime(fecha_inp, '%Y-%m-%d')
            datetime_to_date = fecha_inp_conv.date()
            break
            
        except ValueError:
            print("El formato de fechas es incorrecto. Vuelva a intentarlo: ")
    return datetime_to_date


def input_Graphstyle():
    flag = False
    grf = ""
    while flag == False:
        print('Debe definir un estilo de gráfico: \n 1) Classic \n 2) Charles \n 3) Mike \n 4) Starsandstripes \n 5) Yahoo')
        num = integ_Input("Defina un estilo de gráfico \n:-->")
        
        
        if num > 0 and num <= 5:
            flag = True
            
            if num == 1:
                grf = "classic"
               
            elif num == 2:
                grf = "charles"
            
            elif num == 3:
                grf = "mike"
                
            elif num == 4:
                grf = "starsandstripes"
                
            elif num == 5:
                grf = "yahoo"              

        else:
            print("\n\n El valor ingresado no coincide con los gráficos del programa. Vuelva a ingresarlo nuevamente: ")
    return grf   


def input_Volume():
    flag = False
    grfv = ""
    while flag == False:
        
        num = integ_Input("Desea visualizar el volumen? \n 1) SI \n 2) NO \n:--> ")
        if num > 0 and num <= 2:
            flag = True
            
            if num == 1:
                grfv = True
               
            elif num == 2:
                grfv = False
                           
        else:
            print("\n\n Los valores solo pueden ser 1 o 2. Vuelva a intentar: ")
    return grfv   
        

def input_Mavparams(a):
    
    mavpar = 0
    while True:
        num = integ_Input(a)
        
        if num > 0 and num <= 200:
            mavpar = num
            break          
                          
        else:
            print("\n\n El valor ingresado no es correcto. Vuelva a ingresarlo nuevamente: ")
    return mavpar 

def graph_Visual():
    flag = False
    grfvis = ""
    while flag == False:
        
        num = integ_Input("Desea visualizar la evolución del precio? \n 1) SI \n 2) NO \n:--> ")
        if num > 0 and num <= 2:
            flag = True
            
            if num == 1:
                grfvis = True
               
            elif num == 2:
                grfvis = False
                           
        else:
            print("\n\n Los valores solo pueden ser 1 o 2. Vuelva a intentar: ")
    return grfvis  

def input_Mav():
    flag = False
    grma = ""
    
    while flag == False:
        
        num = integ_Input("Desea agregar medias móviles? \n 1) SI \n 2) NO \n:--> ")
        if num > 0 and num <= 2:
            flag = True
            
            if num == 1:
                grma = True
                               
            elif num == 2:
                grma = False
                           
        else:
            print("\n\n Los valores solo pueden ser 1 o 2. Vuelva a intentar: ")
    return grma           

#-------------------------------------------------------------------------------------
# INICIO EJECUCION DEL PROGRAMA
#-------------------------------------------------------------------------------------

print("INICIO EJECUCION DEL PROGRAMA")


while True:
    ticker = input("Ticker ID: ")
    rango = input_Rango()

    multiplicador = input_Multiplicador(rango)

    
               
    print("Seleccione un rango de fechas formato YYYY-MM-DD para", ticker)


    
    #Validación orden de fechas

    while True:
        fecha_inicio = format_Fechas("Desde: ")
        fecha_fin = format_Fechas("Hasta: ")
        
        if fecha_inicio>fecha_fin:
            print("La fecha inicial no puede ser posterior a la fecha más reciente. Vuelva a intentarlo.")
        
        else:
            break
        
    params = {
           'adjusted':'true',
           'sort':'asc',
           'limit':50000,
           'apiKey':'YpMEdipyjqpz_5JXWVbTom6_YPbxp8ug'
           }


    endpoint="https://api.polygon.io/v2/aggs/ticker/"

       

    url=endpoint+ticker.upper()+"/range/"+multiplicador+"/"+rango+"/"+fecha_inicio.strftime('%Y-%m-%d')+"/"+fecha_fin.strftime('%Y-%m-%d')+"?"
   

    r = requests.get(url,                                                
                    params=params, 
                    verify=True)

    api_response = r.json()
    print(api_response['resultsCount'])
    if api_response['resultsCount'] ==0:
            
        print("No se muestran resultados para el ticker seleccionado.")
    else:
        break


df_response=pd.json_normalize(
     data=api_response,
     record_path='results'
     )

#-------------------------------------------------------------------------------------
# CONEXION A SQLITE
#-------------------------------------------------------------------------------------

#La DB se crea automaticamente. 

conn = sqlite3.connect('marketdata.db')

#La tabla se crea automaticamente y de existir se reemplaza.
df_response.to_sql("stocks", conn, if_exists="replace")
c = conn.cursor()

df_sql = pd.read_sql_query("SELECT * FROM stocks", conn)
print("Los datos fueron ingresados correctamente en la DB")
print(df_sql.head())

c.close()
conn.close()

#-------------------------------------------------------------------------------------
# REARMADO DEL DATAFRAME
#-------------------------------------------------------------------------------------

#Rearmamos la estructura del df para que nos coincida al aplicar las librerias.
#print("DF estructura fuera de linea")
df_estructura=df_sql.loc[:,['t','o','h','l','c','v']].copy()


#en algunas API el campo fecha esta en un formato llamado Epoch o Unix Time
#esta funcion de Pandas nos deja convertir esa columna de ese formato al estandar
#usar el variable explorer para ver como estaba antes y como queda despues
df_estructura['t']=pd.to_datetime(
        df_estructura['t'],
        unit="ms",
        origin="unix"
        )


#Cambiamos el nombre de las columnas para que sean coincidentes con los datos que luego
# necesitará la libreria de graficos

df_estructura.rename(
columns={
    't':'Date',
    'o':'Open',
    'h':'High',
    'l':'Low',
    'c':'Close',
    'v':'Volume'
            }, 
        inplace=True)

print("La estructura del dataframe fue rearmada exitosamente:\n", df_estructura.head())

#-------------------------------------------------------------------------------------
#INICIA VISUALIZACION
#-------------------------------------------------------------------------------------


consulta_graf = graph_Visual()
print("Preparando datos para visualización...")

if consulta_graf == True:
    #Establecemos un indice
    df_estructura=df_estructura.set_index('Date')
    
    #Llamado de funciones
    estilo = input_Graphstyle()
    vol = input_Volume()
    consulta_mav = input_Mav()
    
    if consulta_mav == True:
        print("Seleccione un periodo entre 1 y 200 para cada media móvil.")
        mav1 = input_Mavparams("Media móvil 1: ")
        mav2 = input_Mavparams("Media móvil 2: ")
        mav3 = input_Mavparams("Media móvil 3: ")
        mpf.plot(df_estructura, type='candle', mav = (mav1,mav2,mav3),style='charles',title=ticker, ylabel='Price', volume =True, show_nontrading=False)
        print("Resumen de datos:\n", df_estructura.head())
    else:
        
        mpf.plot(df_estructura, type='candle',style=estilo,title=ticker, ylabel='Price', volume =vol, show_nontrading=False)
        print("Resumen de datos:\n", df_estructura.head())

else:
    
    print("Se procede a guardar los datos sin graficar.")

print("FIN DE EJECUCION DEL PROGRAMA")
