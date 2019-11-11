import requests
import csv 
import pandas as pd
from bs4 import BeautifulSoup

#se definen los géneros (abreviados) y el rango temporal
genres=["AC","BE","C-F","CO","DR","RO","TE","TH","WE"]
years=list(range(2014,2020))

#iniciamos las lista correspondiente a las diferentes variables
lista1=[]
lista2=[]
lista3=[]
lista4=[]
lista5=[]
lista6=[]
lista7=[]
lista8=[]

#definimos la función que guarda la portada de las películas en la carpeta Pictures
def load_requests(source_url):
    r = requests.get(source_url, stream = True)
    aSplit = source_url.split('/')
    ruta="Pictures/"+aSplit[len(aSplit)-1]
    print(ruta)
    output = open(ruta,"wb")
    for chunk in r:
         output.write(chunk)
    output.close()
    return ruta #devolvemos la ruta para asociar cada película a cada imagen


im=0

#para cada género en cada año se buscan (hasta) las 30 películas mejor valoradas
for i in years:
    for j in genres:
        
        
        #se modifica la url dependiendo del género y el año
        url="https://www.filmaffinity.com/es/topgen.php?genre="
        url+=j
        url+="&fromyear="
        url+=str(i)
        url+="&toyear="
        url+=str(i)
        url+="&country=&nodoc&notvse"

        page=requests.get(url)
        soup=BeautifulSoup(page.content,'html.parser')
        
        #scraping de los títulos
        for title in soup.find_all('div',{'class':'mc-title'}):
            lista1.append(title.a.text.strip())
            
            lista2.append(i)
            lista3.append(j)
            
        #scraping de la puntuación     
        for avg in soup.find_all('div',{'class':'avg-rating'}):
            lista4.append(avg.text.strip())
            
        #scraping del número de votos
        for count in soup.find_all('div',{'class':'rat-count'}):
            lista5.append(count.text.strip())
        
        #scraping del nombre del director/a
        for direc in soup.find_all('div',{'class':'mc-director'}):
            lista6.append(direc.text.strip())
        
        #scraping del contenido gráfico
        for pos in soup.find_all('div',{'class':'mc-poster'}):
            lista7.append(pos.img.get('src'))
            if ('static' not in lista7[im]):
                lista8.append(load_requests(lista7[im]))
            im=im+1
        
#se añaden al dataframe las diferentes variables
df=pd.DataFrame([lista1,lista2,lista3,lista4,lista5,lista6,lista7,lista8])
df=df.T #es necesario transponer la matriz del dataframe para obtener el formato adecuado

#definimos el nombre de las variables (columnas)
col=["Título","Año","Género","Puntuación","N_Votos","Director/a","Local_portada","Web_portada"]

#exportamos a un fichero csv
df.to_csv('films.csv',header=col,index=False)