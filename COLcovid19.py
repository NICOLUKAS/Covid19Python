# Importamos las librerias a usuar en el programa
from getpass import getuser
import requests
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import geojson 

#GRÁFICOS COLOMBIA
def descargarColombia():
    url = 'https://www.datos.gov.co/api/views/gt2j-8ykr/rows.csv?accessType=DOWNLOAD'
    myfile = requests.get(url,allow_redirects=True)
    open('C:/Users/'+getuser()+'/Downloads/Casos_positivos_de_COVID-19_en_Colombia.csv','wb').write(myfile.content)
    

def extraerDataColombia():
    url = 'C:/Users/'+getuser()+'/Downloads/Casos_positivos_de_COVID-19_en_Colombia.csv'
    datos=pd.read_csv(url)
    df=pd.DataFrame(datos)
    #Grafico barra: Departamento vs Recuperados
    df1=df[df['atención']=='Recuperado']
    df1.groupby(['Departamento o Distrito ']) ['atención'].count().plot(kind='bar',legend='Reverse')
    plt.title('Departamentos vs Recuperados')
    plt.ylabel('Número Casos Recuperados')
    plt.show()
    #Grafico barro: Departamento vs Fallecidos
    df2=df[df['atención']=='Fallecido']
    df2.groupby(['Departamento o Distrito ']) ['atención'].count().plot(kind='bar',legend='Reverse')
    plt.title('Departamentos vs Fallecidos')
    plt.ylabel('Número Casos Fallecidos')
    plt.show()
    #Grafico barra: Departamento vs Contagiados
    df3=df[(df['atención']=='Casa') | (df['atención']=='Hospital UCI') | (df['atención']=='Hospital') | (df['atención']=='Fallecido') | (df['atención']=='Recuperado')] 
    df3.groupby(['Departamento o Distrito ']) ['atención'].count().plot(kind='bar',legend='Reverse')
    plt.title('Departamentos vs Confirmados')
    plt.ylabel('Número Casos Confirmados')
    plt.show()
    #Grafico torta: Activos
    df4= df[(df['atención']=='Casa') | (df['atención']=='Hospital UCI') | (df['atención']=='Hospital')]
    colores = ["#0C3271","#638DD4","#DBE3EF"]
    df4.groupby(['atención']) ['atención'].count().plot(kind="pie", autopct="%0.1f %%",colors=colores)
    plt.title('Casos Activos')
    plt.ylabel('')
    plt.show()
    #Grafico torta: Confirmados
    df5= df[(df['atención']=='Casa') | (df['atención']=='Hospital UCI') | (df['atención']=='Hospital') | (df['atención']=='Fallecido') | (df['atención']=='Recuperado')] 
    df5=df5.reset_index(drop=True)
    for i in range(0,len(df5)):
        if (df5.loc[i,'atención']=='Casa') | (df5.loc[i,'atención']=='Hospital UCI') | (df5.loc[i,'atención']=='Hospital'):
            df5.loc[i,'atención']='Activo'
       
    colores = ["#0C3271","#638DD4","#DBE3EF"]
    df5.groupby(['atención']) ['atención'].count().plot(kind="pie", autopct="%0.1f %%",colors=colores)
    plt.title('Casos Confirmados')
    plt.ylabel('')
    plt.show()

#MAPAS COLOMBIA
def datosMapasColombia():
    url = 'C:/Users/'+getuser()+'/Downloads/Casos_positivos_de_COVID-19_en_Colombia.csv'
    datos=pd.read_csv(url)
    df=pd.DataFrame(datos)
    #Dataframe
    df1= df[(df['atención']=='Casa') | (df['atención']=='Hospital UCI') | (df['atención']=='Hospital') | (df['atención']=='Fallecido') | (df['atención']=='Recuperado')] 
    df2=pd.DataFrame()
    df2=df1[['Departamento o Distrito ','atención']]
    df3=pd.DataFrame({'count' : df2.groupby(['Departamento o Distrito ']) ['atención'].size()}).reset_index()
    df3.to_csv('C:/Users/'+getuser()+'/Downloads/Departamentos.csv')


def MapasColombia():
    #Archivo CSV
    url = 'C:/Users/'+getuser()+'/Downloads/Departamentos.csv'
    datos=pd.read_csv(url)
    df=pd.DataFrame(datos)
    #df=df.fillna(method='ffill')
    df['Departamento o Distrito ']=df['Departamento o Distrito '].str.upper()
    for i in range(0,len(df)):
        if df.loc[i,'Departamento o Distrito ']=='BOGOTÁ D.C.':
            df.loc[i,'Departamento o Distrito ']='SANTAFE DE BOGOTA D.C'
        elif df.loc[i,'Departamento o Distrito ']=='CAQUETÁ':
            df.loc[i,'Departamento o Distrito ']='CAQUETA'
        elif df.loc[i,'Departamento o Distrito ']=='VAUPÉS':
            df.loc[i,'Departamento o Distrito ']='VAUPES'
        elif df.loc[i,'Departamento o Distrito ']=='GUAINÍA':
            df.loc[i,'Departamento o Distrito ']='GUAINIA'
        elif df.loc[i,'Departamento o Distrito ']=='QUINDÍO':
            df.loc[i,'Departamento o Distrito ']='QUINDIO'
        elif df.loc[i,'Departamento o Distrito ']=='CHOCÓ':
                df.loc[i,'Departamento o Distrito ']='CHOCO'    
        elif df.loc[i,'Departamento o Distrito ']=='BOYACÁ':
                df.loc[i,'Departamento o Distrito ']='BOYACA'  
        elif df.loc[i,'Departamento o Distrito ']=='BOLÍVAR':
                df.loc[i,'Departamento o Distrito ']='BOLIVAR'    
        elif df.loc[i,'Departamento o Distrito ']=='CÓRDOBA':
                df.loc[i,'Departamento o Distrito ']='CORDOBA'         
        elif df.loc[i,'Departamento o Distrito ']=='ARCHIPIÉLAGO DE SAN ANDRÉS PROVIDENCIA Y SANTA CATALINA':
                df.loc[i,'Departamento o Distrito ']='ARCHIPIELAGO DE SAN ANDRES PROVIDENCIA Y SANTA CATALINA'            
        elif df.loc[i,'Departamento o Distrito ']=='ATLÁNTICO':
                df.loc[i,'Departamento o Distrito ']='ATLANTICO'
    
    #Archivo json()
    reque_url = 'https://gist.githubusercontent.com/john-guerra/43c7656821069d00dcbc/raw/3aadedf47badbdac823b00dbe259f6bc6d9e1899/colombia.geo.json'
    co_departamentos_geo=requests.get(reque_url).json()
    
    fig = px.choropleth(data_frame=df,
                        geojson=co_departamentos_geo,
                        locations='Departamento o Distrito ',
                        featureidkey='properties.NOMBRE_DPT',
                        color='count',
                        color_continuous_scale="burg"
                       )
    
    fig.update_geos(showcountries=True, showcoastlines=True, showland=True, fitbounds="locations")

    fig.update_layout(
        title_text = 'Casos Covid Activos Colombia',
        font=dict(
            family="Arial",
            size=18,
            color="#7f7f7f"
                 )

                     )
    fig.show()


#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

#GRÁFICOS BOGOTÁ
def descargarBogota():
    url = 'https://datosabiertos.bogota.gov.co/dataset/44eacdb7-a535-45ed-be03-16dbbea6f6da/resource/b64ba3c4-9e41-41b8-b3fd-2da21d627558/download/osb_enftransm-covid-19.csv'
    myfile = requests.get(url,allow_redirects=True)
    open('C:/Users/'+getuser()+'/Downloads/osb_enftransm-covid-19.csv','wb').write(myfile.content)

def extraerDataBogota():
    url = 'C:/Users/'+getuser()+'/Downloads/osb_enftransm-covid-19.csv'
    datos=pd.read_csv(url,encoding='latin-1')
    df=pd.DataFrame(datos)
    #Gráfico hombres mujeres recuperados
    df1=df[df['Estado']=='Recuperado'] 
    colores = ["#0C3271","#638DD4","#DBE3EF"]
    df1.groupby(['Sexo']) ['Estado'].count().plot(kind="pie", autopct="%0.1f %%",colors=colores)
    plt.title('Hombres y Mujeres - Recuperados')
    plt.show()
    #Gráfico Localidad vs Fallecidos
    df2=df[df['Estado']=='Fallecido']
    df2.groupby(['Localidad de residencia']) ['Estado'].count().plot(kind='bar',legend='Reverse')
    plt.title('Localidades vs Fallecidos')
    plt.ylabel('Número Casos Fallecidos')
    plt.show()
    #Gráfico general ubicación
    df3=df[(df['Ubicación']=='Casa') | (df['Ubicación']=='Hospital UCI') | (df['Ubicación']=='Hospital UCI Intermedia') | (df['Ubicación']=='Hospital') | (df['Ubicación']=='Fallecido No aplica No causa Directa') | (df['Ubicación']=='Fallecido')]
    df3.groupby(['Ubicación']) ['Ubicación'].count().plot(kind="pie", autopct="%0.1f %%")
    plt.title('Casos por ubicación')
    plt.show()

#MAPAS BOGOTÁ
def datosMapasBogota():
    url = 'C:/Users/'+getuser()+'/Downloads/osb_enftransm-covid-19.csv'
    datos=pd.read_csv(url,encoding='latin-1') 
    df=pd.DataFrame(datos)
    df1=df[['Localidad de residencia']]
    df2=pd.DataFrame({'count' : df1.groupby(['Localidad de residencia']).size()}).reset_index()
    df2.to_csv('C:/Users/'+getuser()+'/Downloads/Localidades.csv')

def MapasBogota():
    #Archivo CSV
    url = 'C:/Users/'+getuser()+'/Downloads/Localidades.csv'
    datos=pd.read_csv(url)
    df=pd.DataFrame(datos)
    df['Localidad de residencia']=df['Localidad de residencia'].str.upper()
    for i in range(0,len(df)):
        if df.loc[i,'Localidad de residencia']=='CIUDAD BOLÍVAR':
            df.loc[i,'Localidad de residencia']='CIUDAD BOLIVAR'
        elif df.loc[i,'Localidad de residencia']=='ENGATIVÁ':
            df.loc[i,'Localidad de residencia']='ENGATIVA'
        elif df.loc[i,'Localidad de residencia']=='FONTIBÓN':
            df.loc[i,'Localidad de residencia']='FONTIBON'
        elif df.loc[i,'Localidad de residencia']=='LA CANDELARIA':
            df.loc[i,'Localidad de residencia']='CANDELARIA'
        elif df.loc[i,'Localidad de residencia']=='LOS MÁRTIRES':
            df.loc[i,'Localidad de residencia']='LOS MARTIRES'
        elif df.loc[i,'Localidad de residencia']=='SAN CRISTÓBAL':
            df.loc[i,'Localidad de residencia']='SAN CRISTOBAL'
        elif df.loc[i,'Localidad de residencia']=='USAQUÉN':
            df.loc[i,'Localidad de residencia']='USAQUEN'
        elif df.loc[i,'Localidad de residencia']=='ANTONIO NARIÑO':
            df.loc[i,'Localidad de residencia']='ANTONIO NARINO'

    #Archivo json()
    with open ('bogota_localidades (1).geojson') as file:
        data = geojson.load(file)

    fig = px.choropleth(data_frame=df,
                        geojson=data,
                        locations='Localidad de residencia',
                        featureidkey='properties.NOMBRE',
                        color='count',
                        color_continuous_scale="burg"
                       )
    
    fig.update_geos(showcountries=True, showcoastlines=True, showland=True, fitbounds="locations")

    fig.update_layout(
        title_text = 'Casos Covid Bogotá',
        font=dict(
            family="Arial",
            size=18,
            color="#7f7f7f"
                 )

                     )
    fig.show()


descargarColombia()
#extraerDataColombia()
datosMapasColombia()
MapasColombia()
descargarBogota()
extraerDataBogota()
datosMapasBogota()
MapasBogota()


