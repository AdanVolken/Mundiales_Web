from bs4 import BeautifulSoup
import requests
import pandas as pd

años = [1930, 1934, 1938, 1950, 1954, 1958, 1962, 1966, 1970, 1974,
         1978, 1982, 1986, 1990, 1994, 1998, 2002, 2006, 2010, 2014,
         2018, 2022]

def obtener_partidos(año):
    web = f"https://en.wikipedia.org/wiki/{año}_FIFA_World_Cup"

    respuesta = requests.get(web).text #Obtenemos el codigo fuente de la pagina web

    # print(respuesta)
    soup = BeautifulSoup(respuesta, "lxml")

    partidos = soup.find_all('div', class_= "footballbox")


    # creamos listas para guardar los resultados
    local = []
    resultado = []
    visitante =  []


    for partido in partidos:
        local.append(partido.find('th', class_= 'fhome').get_text())  # equipo local
        resultado.append(partido.find('th', class_= 'fscore').get_text())  # resultado
        visitante.append(partido.find('th', class_= 'faway').get_text()) # eqipo visitante

    # Diccionario para crear el df

    dict_mundial = {
        "local": local,
        "resultado": resultado ,
        'visitante': visitante
    }

    df_mundial = pd.DataFrame(dict_mundial)
    df_mundial["año"] = año

    return df_mundial

fifa = [obtener_partidos(año) for año in años]

df_fifa = pd.concat(fifa, ignore_index=True)
df_fifa.to_csv("partidos_mundiales.csv")

print( "CSV Creado correctamente ")