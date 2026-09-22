# Archivo base para el despliegue del Agente en Streamlit.
# Librerias a importar
import streamlit as st
from sklearn.linear_model import LinearRegression
import numpy as np

# Titulo
st.title("Configuracion inicial")
# Textbox
st.write("Primera prueba de uso de streamlit y ambiente de MA2026")
# EL slider de stremlit 
gasto=st.slider("Seleccine nivel de gasto en publicicdad", 10,200,50)

# Variables
variable_x = np.array([[10], [20], [30], [40],[50]])
variable_y = np.array([15,25,35,45,55])
modelo_lr = LinearRegression()

#Entrenamiento
modelo_lr.fit(variable_x,variable_y)

# Boton de predecir y activa el if
if st.button("Predecir"):
    resultado = modelo_lr.predict([[gasto]])
    # Mensaje de exito
    st.success(f"Las ventas proyectadas para una inversion de ${gasto} son: ${resultado[0]}")