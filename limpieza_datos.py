import pandas as pd
import streamlit as st

st.title("Limpieza de Datos")
ruta = "https://raw.githubusercontent.com/VMjavier/claseAnalisisDatos/refs/heads/main/veterinaria_colombia.csv"

df = pd.read_csv(ruta)
st.write(df)

st.subheader("1.Columnas del Dataset")
st.write(df.columns)

st.subheader("2. Valores nulos por columna")
nulos = df.isnull().sum().reset_index()
nulos.columns = ['Columna', 'Valores Nulos']
st.write(nulos)

st.subheader("3. Dimensiones del Dataset")
filas, columnas = df.shape
c1, c2 = st.columns(2)
c1.metric("Filas", filas)
c2.metric("Columnas", columnas)

#cambiar las columnas a minúsculas y sin espacios
df.columns = df.columns.str.lower().str.replace(' ', '_')

#cambiar el nombre de la columna particular 
df.rename(columns = {"nombre": "nombre_mascota"}, inplace = True)

st.subheader("4. Columnas del Dataset después de la limpieza")
st.write(df.columns)

#eliminar filas y colomnas completamente nulas
df.dropna(axis=0, how='all', inplace=True) #fila = 0
df.dropna(axis=1, how='all', inplace=True) #columna = 1

st.subheader("5. dimensiones del dataset nuevas")
filas, columnas = df.shape
c1, c2 = st.columns(2)
c1.metric("Filas", filas)
c2.metric("Columnas", columnas)

#elininar columnas especificas
df.drop(columns = ["nombre_mascota"], inplace = True)

st.subheader("6. dataset limpieza parcial")
st.write(df)