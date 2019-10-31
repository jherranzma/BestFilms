import requests
import csv 
import pandas as pd
from bs4 import BeautifulSoup

#se definen los géneros (abreviados) y el rango temporal
genres=["AC","BE","C-F","CO","DR","RO","TE","TH","WE"]
years=list(range(1999,2020))

lista1=[]
lista2=[]
lista3=[]
lista4=[]
lista5=[]
lista6=[]

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

df=pd.DataFrame([lista1,lista2,lista3,lista4,lista5,lista6])
df=df.T
df
col=["Título","Año","Género","Puntuación","N_Votos","Director/a"]
df.to_csv('films.csv',header=col,index=False)